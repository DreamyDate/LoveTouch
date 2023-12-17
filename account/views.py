from django.shortcuts import get_object_or_404
from .models import StatusFavorite
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import ImageFile
from easy_thumbnails.files import get_thumbnailer
from datetime import timedelta
from .forms import (LoginForm, UserRegistrationForm, UserEditForm,
                    ProfileEditForm, SocialLinkForm, StatusForm, StatusCommentForm, ProfileEditRelationship, ProfileAppearanceForm, ProfileEducationForm)
from .models import (Profile,  Status, StatusComment,
                     StatusLike, PremiumPackage, PremiumPurchase, StatusFavorite)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
from .filters import UserFilter
from .models import CreditTransaction
import stripe
from django.conf import settings
from dating.models import Match
from datetime import timedelta
from albums.models import Photo
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from notifications.models import Notification
from chat_app.models import Message, Room
from cities_light.models import City
from django.http import HttpResponseForbidden
from django.utils.translation import get_language
from django.core.exceptions import ValidationError
from django.db.models import Q
from chat_app.utils.message_utils import count_total_unread_messages
from django.db.models import Max
from gift.models import GiftPurchase
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.templatetags.static import static


stripe.api_key = settings.STRIPE_SECRET_KEY

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'message': 'Authenticated successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Disabled account'}, status=403)
            else:
                return JsonResponse({'error': 'Invalid login'}, status=400)
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def home(request):
    # Получаем список активных пользователей и применяем фильтр к нему
    user_list = User.objects.filter(is_active=True)
    user_filter = UserFilter(request.GET, queryset=user_list)
    users = user_filter.qs

    statuses = Status.objects.filter(user=request.user).order_by('-creation_date')
    # Получаем друзей текущего пользователя
    friends = request.user.profile.friends.all()

    # Фильтруем друзей по дате рождения
    todays_birthdays = friends.filter(date_of_birth__month=date.today().month,
                                  date_of_birth__day=date.today().day)
  
    # Словарь для комментариев каждого статуса
    comments_dict = {}

    # Добавим атрибут для каждого статуса, указывающий, лайкнул ли текущий пользователь этот статус
    for status in statuses:
        comments_dict[status.id] = StatusComment.objects.filter(status=status).order_by('created_date')[:5]
        status_comments_count = StatusComment.objects.filter(status=status).order_by('created_date').count()
        status.has_more_than_five_comments = status_comments_count >= 5
        status.liked_by_current_user = status.is_liked_by(request.user)

    comment_form = StatusCommentForm()

    if request.method == "POST":
        if 'post_comment' in request.POST:
            comment_form = StatusCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                status_id = request.POST.get('status_id')
                comment.status = get_object_or_404(Status, id=status_id)
                try:
                    comment.save()
                except Exception as e:
                    print(f"Error saving comment: {e}")

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    updated_status = get_object_or_404(Status, id=status_id)
                    user_photo_url = comment.user.profile.photo.url if comment.user.profile.photo else static(
                        'images/affect.jpg')
                    return JsonResponse({
                       "success": True,
                       "message": "Comment added successfully.",
                       "status_id": status_id,
                       "comments_count": updated_status.comments_count,
                       "comment": {
                           "user": {
                               "photo": {
                                   "url": user_photo_url
                               },
                               "username": comment.user.username
                           },
                           "text": comment.text,
                           "created_date": comment.created_date.strftime('%Y-%m-%d %H:%M:%S')
                       }
                    })
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "errors": comment_form.errors})
        elif 'edit_status' in request.POST:
            status_id = request.POST.get('status_id')
            status_content = request.POST.get('status_content')
            
            status_to_edit = get_object_or_404(Status, id=status_id)
            
            if status_to_edit.user != request.user:
                return JsonResponse({"success": False, "message": "Insufficient rights to edit."})
            
            status_to_edit.content = status_content
            status_to_edit.save()
            
            return JsonResponse({"success": True, "message": "Status updated successfully."})
        
    friends_online = request.user.profile.friends_online()

    online_users_count = len(friends_online)
    
    potential_friends = get_potential_friends(request.user.profile)[:15]  # Получаем 15 потенциальных друзей

    current_month = date.today().month
    current_day = date.today().day

    # Если хотите исключить уже прошедшие дни рождения в этом месяце:
    upcoming_birthdays = friends.filter(date_of_birth__month=current_month, date_of_birth__day__gt=current_day).order_by('date_of_birth__day')
   # Определите начальное и конечное время (24 часа назад от текущего времени).
    end_time = timezone.now()
    start_time = end_time - timezone.timedelta(days=1)

    # Получите последние статусы опубликованные в течение последних 24 часов.
    type_filter = Q(type='photo') | Q(type='video')
    recent_statuses = Status.objects.filter(Q(creation_date__range=(start_time, end_time)) & type_filter).order_by('-creation_date')
   
    # Получите все статусы всех пользователей
    all_statuses = Status.objects.all().order_by('-creation_date')

   
    
    context = {
        'users': users,
        'statuses': statuses,
        'comments_dict': comments_dict,  
        'form': StatusForm(),
        'comment_form': comment_form,
        'todays_birthdays': todays_birthdays,
        'user_filter': user_filter,  # передаем фильтр в контекст
        'friends_online': friends_online,
        'online_users_count': online_users_count,
        'potential_friends': potential_friends,
        'upcoming_birthdays': upcoming_birthdays,
        'recent_statuses': recent_statuses, 
        
        'all_statuses': all_statuses,
        
    }
    
    return render(request, 'account/home.html', context)

def get_potential_friends(profile):
    # Получить всех друзей текущего пользователя
    friends = profile.friends.all()

    # Исключить из всех профилей друзей текущего пользователя и самого пользователя
    potential_friends = Profile.objects.exclude(id__in=friends.values_list('id', flat=True)).exclude(id=profile.id)
    
    return potential_friends

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.is_active = False  # Устанавливаем пользователя как неактивного
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Создаем токен подтверждения
            token = default_token_generator.make_token(new_user)
            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            domain = get_current_site(request).domain
            link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})

            confirm_url = 'http://{}{}'.format(domain, link)

            # Отправляем токен на электронную почту пользователя
            send_mail(
                'Confirm your email',
                'Follow the link to confirm: {}'.format(confirm_url),
                'noreply@yourdomain.com',
                [new_user.email],
                fail_silently=False,
            )

            # Создаем профиль пользователя и сохраняем дополнительные данные
            profile = Profile.objects.create(
                user=new_user, 
                gender=user_form.cleaned_data['gender'], 
                date_of_birth=user_form.cleaned_data['date_of_birth'], 
                relationship_goals=user_form.cleaned_data['relationship_goals']
            )

            return redirect('login') 
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'user_form': user_form})

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/register.html')

@login_required
def edit(request):
    if hasattr(request.user, 'sociallink'):
        social_link_instance = request.user.sociallink
    else:
        social_link_instance = None

    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    social_link_form = SocialLinkForm(instance=social_link_instance)
    password_form = PasswordChangeForm(request.user)
    profile_form_relationship = ProfileEditRelationship(instance=request.user.profile)
    profile_form_appearance = ProfileAppearanceForm(
        instance=request.user.profile)
    profile_form_education = ProfileEducationForm(
        instance=request.user.profile)
    selected_city_name = City.objects.get(id=request.user.profile.city_id).name if request.user.profile.city_id else None


    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'social_link':
            social_link_form = SocialLinkForm(instance=social_link_instance, data=request.POST)
            if social_link_form.is_valid():
                social_link_form.save()
                messages.success(request, 'Social links updated successfully')
                return redirect('edit')
            else:
                messages.error(request, 'Error updating social links')

        elif form_type == 'user_info':
            user_form = UserEditForm(instance=request.user, data=request.POST)
           
            if user_form.is_valid():
                user_form.save()
                
                messages.success(request, 'Profile updated successfully')
                return redirect('edit')
            else:
                messages.error(request, 'Error updating your profile')
        
        elif form_type == 'user_info_all':
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            
            if profile_form.is_valid():
                               
                profile_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('edit')

            else:
                print(profile_form.errors)

                errors = profile_form.errors.as_text()
                messages.error(request, f'Error updating your profile. Errors: {errors}')

        elif form_type == 'user_info_relationship':
            profile_form_relationship = ProfileEditRelationship(
                instance=request.user.profile, data=request.POST, files=request.FILES)

            if profile_form_relationship.is_valid():

                profile_form_relationship.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('edit')

            else:
                print(profile_form_relationship.errors)

                errors = profile_form_relationship.errors.as_text()
                messages.error(
                    request, f'Error updating your profile. Errors: {errors}')
                
        elif form_type == 'user_info_appearance':
            profile_form_appearance = ProfileAppearanceForm(
                instance=request.user.profile, data=request.POST, files=request.FILES)

            if profile_form_appearance.is_valid():

                profile_form_appearance.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('edit')

            else:
                print(profile_form_appearance.errors)

                errors = profile_form_appearance.errors.as_text()
                messages.error(
                    request, f'Error updating your profile. Errors: {errors}')
                
        elif form_type == 'user_info_education':
            profile_form_education = ProfileEducationForm(
                instance=request.user.profile, data=request.POST, files=request.FILES)

            if profile_form_education.is_valid():

                profile_form_education.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('edit')

            else:
                print(profile_form_education.errors)

                errors = profile_form_education.errors.as_text()
                messages.error(
                    request, f'Error updating your profile. Errors: {errors}')
                


        elif form_type == 'password_change':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('edit')
            else:
                messages.error(request, 'Please correct the error below.')

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'profile_form_relationship': profile_form_relationship, 'profile_form_appearance': profile_form_appearance, 'profile_form_education': profile_form_education, 'social_link_form': social_link_form,
                                                 'password_form': password_form,
                                                  'selected_city_name': selected_city_name,})

@login_required
def user_detail(request, username):
    # Получаем пользователя на основе переданного username (выбранного пользователя)
    selected_user = get_object_or_404(User, username=username, is_active=True)
    
    # Получаем профиль выбранного пользователя
    selected_profile = get_object_or_404(Profile, user=selected_user)

    # Также получаем профиль текущего авторизованного пользователя
    profile = get_object_or_404(Profile, user=request.user)
    user_statuses = Status.objects.filter(
        user=selected_user).order_by('-creation_date')
   
    selected_user_friends = selected_profile.friends.all()
    time_threshold = timezone.now() - timedelta(minutes=5)
    online_friends = selected_profile.friends.filter(last_activity__gte=time_threshold)
    
    # Проверяем, является ли выбранный пользователь текущим авторизованным пользователем
    is_current_user_profile = selected_user == request.user
    
    # Проверяем, является ли выбранный пользователь другом текущего пользователя
    is_friend = selected_profile.friends.filter(id=request.user.id).exists()
    
    # Проверяем, подписан ли выбранный пользователь на текущего пользователя
    is_following = selected_profile.following_set.filter(id=request.user.id).exists()
    
    for friend in selected_user_friends:
        friend.follower_count = friend.followers.count()  # Предположим, что `followers` - это обратная связь
    
    for friend in selected_user_friends:
        friend.is_current_user_friend = profile.friends.filter(id=friend.id).exists()
        friend.is_current_user_following = profile.following_set.filter(id=friend.id).exists()
        friend.is_current_user = friend.user == request.user
    
    photos = Photo.objects.filter(user=selected_user)

    photos_count = Photo.objects.filter(user=selected_user).count()
    recent_photos = Photo.objects.filter(user=selected_user).order_by('-created_at')
    favorite_photos = Photo.objects.filter(favorites__user=selected_user)
    favorite_photos_count = Photo.objects.filter(favorites__user=selected_user).count()
    received_gifts = GiftPurchase.objects.filter(recipient=selected_user)

    # Словарь для комментариев каждого статуса
    comments_dict = {}

    # Добавим атрибут для каждого статуса, указывающий, лайкнул ли текущий пользователь этот статус
    for status in user_statuses:
        comments_dict[status.id] = StatusComment.objects.filter(
            status=status).order_by('created_date')[:5]
        status_comments_count = StatusComment.objects.filter(
            status=status).order_by('created_date').count()
        status.has_more_than_five_comments = status_comments_count >= 5
        status.liked_by_current_user = status.is_liked_by(request.user)

    comment_form = StatusCommentForm()


    # Передаем переменные в контекст шаблона и отображаем страницу
    return render(request,
                  'account/user/user_detail.html',
                  {
                   'selected_user': selected_user,
                   'selected_profile': selected_profile,
                   'profile': profile,
                   'is_current_user_profile': is_current_user_profile,
                   'selected_user_friends': selected_user_friends,
                   'online_friends': online_friends,
                   'following_count': selected_profile.following_count(),
                   'is_friend': is_friend,
                   'is_following': is_following,
                   'photos': photos,
                   'photos_count': photos_count,
                   'recent_photos':recent_photos,
                   'favorite_photos': favorite_photos,
                   'favorite_photos_count': favorite_photos_count,
                   'received_gifts': received_gifts,  # Передаем список подарков
                   'user_statuses': user_statuses,
                   'comments_dict': comments_dict,
                   'comment_form': comment_form,

                  })


def upload_avatar(request):
    # Проверка метода
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    # Проверка авторизованности пользователя
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)
    
    # Проверка наличия файла в запросе
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)

    file = request.FILES['file']

    # Проверка типа файла (простейший пример)
    if not file.content_type.startswith('image/'):
        return JsonResponse({'error': 'Invalid file type. Please upload an image.'}, status=400)

    profile = request.user.profile
    profile.photo = ImageFile(file)
    profile.save()

    options = {'size': (180, 180), 'crop': True}
    thumbnailer = get_thumbnailer(profile.photo)
    thumbnail_url = thumbnailer.get_thumbnail(options).url

    return JsonResponse({'image_url': thumbnail_url})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/edit.html', {'form': form})

@login_required
def add_status(request):
    if request.method == "POST":
        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.expiration_date = timezone.now() + timedelta(hours=24)
            if 'fileInput' in request.FILES:
                status.file = request.FILES['fileInput']
            status.type = request.POST.get('type')
            try:
                status.save()
                messages.success(request, 'The status has been created successfully.')
                return redirect('home')
               
            except ValidationError as e:
                messages.error(request, e.message)
            
            
        else:
            context = {'form': form}
            return redirect('home')
    else:
        form = StatusForm()
    return redirect('home')

def view_status(request):
    if request.user.is_authenticated:
        statuses = (Status.objects.filter(user=request.user, expiration_date__gt=timezone.now())
                    .select_related('user'))  # оптимизация запроса к базе данных
    else:
        statuses = []
    return render(request, 'account/home.html', {'statuses': statuses})

def create_comment(user, status, text):
    comment = StatusComment(user=user, status=status, text=text)
    comment.save()


def like_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    status.like(request.user)
    # Redirect или ответ, в зависимости от вашей логики
def unlike_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    status.unlike(request.user)
    # Redirect или ответ, в зависимости от вашей логики

@login_required
def update_like_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    
    if StatusLike.objects.filter(user=request.user, status=status).exists():
        # Если пользователь уже поставил лайк, удаляем его
        status.unlike(request.user)
        liked = False
    else:
        # Иначе добавляем лайк
        status.like(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'likes_count': status.likes_count})

# Utility function to format comment date based on language

def format_comment_date(dt):
    #Format the comment date based on the current active language.""""""
    current_language = get_language()  # Получает текущий активный язык

    if current_language == "ru":
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Формат по умолчанию или для других языков
        return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_comments(request, status_id):
    load_all = request.GET.get('loadAll') == 'true'
    
    if load_all:
        comments = StatusComment.objects.filter(status_id=status_id).order_by('created_date')
    else:
        comments = StatusComment.objects.filter(status_id=status_id).order_by('created_date')[:5]
    
    comments_data = [
        {
            'username': comment.user.username,
            'photo_url': comment.user.profile.photo.url if comment.user.profile.photo else static('images/affect.jpg'),
            'text': comment.text,
            'created_date': format_comment_date(comment.created_date)
        } 
        for comment in comments
    ]
    
    return JsonResponse({'success': True, 'comments': comments_data})


@login_required
def delete_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)

    # Проверка прав пользователя на удаление
    if status.user != request.user:
        messages.error(request, "Insufficient permissions to delete.")
        return redirect('home')  # предположим, что 'home' - это имя вашего URL-паттерна для главной страницы

    status.delete_status()
    messages.success(request, "The status was successfully deleted.")
    return redirect('home')

@login_required
def toggle_comments(request, status_id):
    status = get_object_or_404(Status, id=status_id)

    # Проверка прав пользователя на изменение
    if status.user != request.user:
        messages.error(request, "Insufficient rights to change status.")
        return redirect('home')

    # Переключаем значение comments_enabled
    status.comments_enabled = not status.comments_enabled
    status.save()
    
    message = "Comments are disabled." if not status.comments_enabled else "Comments included."
    messages.success(request, message)

    return redirect('home')


@login_required
def edit_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    
    # Проверка прав пользователя на редактирование
    if status.user != request.user:
        messages.error(request,"Insufficient rights to edit.")

    if request.method == "POST":
        form = StatusForm(request.POST, request.FILES, instance=status)
        if form.is_valid():
            form.save()
            return redirect('home')  # redirecting to the home page after successful editing
    else:
        form = StatusForm(instance=status)

    context = {
        'form': form,
        'status': status,
    }

    return render(request, 'account/edit_status.html', context)


def add_credits(user, amount, stripeToken, description=""):
    # Проведение платежа с использованием Stripe
    try:
        charge = stripe.Charge.create(
            amount=int(amount * 100),  
            currency='usd',
            description=description,
            source=stripeToken
        )
    except stripe.error.CardError as e:
        # Если была ошибка с картой
        raise ValueError("Ошибка карты: {}".format(e))

    if charge.paid:
        profile = user.profile  # Получите профиль пользователя
        profile.credits += amount
        profile.save()
        CreditTransaction.objects.create(user=profile, amount=amount, transaction_type='C', description=description)
    else:
        raise ValueError("Error when making a payment via Stripe.")
    

def purchase_credits(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Access is denied. Please login.")

    if request.method == "POST":
        user = request.user
        amount = int(request.POST.get("amount"))
        stripeToken = request.POST.get("stripeToken")

        try:
            add_credits(user, amount, stripeToken, description=f"Replenishment of credits for the user {user.username}")
            return render(request, 'setings/pay_stripe.html', {})
        
        except stripe.error.CardError as e:
            return JsonResponse({"status": "fail", "message": str(e.user_message)})
        except ValueError as e:
            return JsonResponse({"status": "fail", "message": str(e)})
    else:
        return render(request, 'setings/pay_stripe.html', {})


def deduct_credits(user, amount, description=""):
    profile = user.profile
    if profile.credits < amount:
        raise ValueError("Not enough credits.")
    profile.credits -= amount
    profile.save()
    CreditTransaction.objects.create(user=profile, amount=amount, transaction_type='D', description=description)

def list_premium_packages(request):
    packages = PremiumPackage.objects.all()
    
    return render(request, 'account/upgrade.html', {'packages': packages})

def buy_premium_package(request, package_id):
    package = get_object_or_404(PremiumPackage, id=package_id)
    profile = request.user.profile
    if request.method == "POST":
        try:
            # Попытка списать кредиты за покупку пакета
            deduct_credits(request.user, package.price, description=f"Purchasing a package {package.title}")

            # Проверка, есть ли у пользователя запись пакета Premium
            current_premium_purchase = PremiumPurchase.objects.filter(profile=profile).order_by('-expiry_date').first()
            
            # Если у пользователя есть пакет Premium и он еще активен
            if current_premium_purchase and current_premium_purchase.expiry_date > timezone.now():
                current_premium_purchase.expiry_date += timedelta(days=package.duration)  # Продлеваем дату истечения
                current_premium_purchase.package = package  # Обновляем пакет
                current_premium_purchase.save()
            elif current_premium_purchase and current_premium_purchase.expiry_date <= timezone.now():
                # Если пакет неактивен
                current_premium_purchase.expiry_date = timezone.now() + timedelta(days=package.duration)
                current_premium_purchase.package = package  # Обновляем пакет
                current_premium_purchase.save()
            else:
                # Если у пользователя нет пакета Premium, создаем новую запись
                PremiumPurchase.objects.create(
                    profile=profile,
                    package=package,
                    expiry_date=timezone.now() + timedelta(days=package.duration)
                )
            messages.success(request, 'Successful purchase of the premium package!')
            return redirect('home')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'account/upgrade.html', {'package': package})


@login_required
def activity_categories(request):
    user = request.user.profile
    
    viewed_profiles = user.viewers.all()
    matched_profiles = user.initiated_matches.filter(is_confirmed_by_user1=True, is_confirmed_by_user2=True).values_list('user2', flat=True)
    favorite_contacts = user.friends.all()
    liked_profiles = user.liked_by.all()
    liked_by_profiles = Profile.objects.filter(liked_by=request.user)
    
    context = {
        'viewed_profiles': viewed_profiles,
        'matched_profiles': matched_profiles,
        'favorite_contacts': favorite_contacts,
        'liked_profiles': liked_profiles,
        'liked_by_profiles': liked_by_profiles,
    }
    
    return render(request, 'account/user/activity_categories.html', context)

@login_required
def add_to_viewed_profiles(request, profile_id):
    profile_to_add = get_object_or_404(Profile, id=profile_id)
    request.user.profile.add_viewer(profile_to_add.user)
    return redirect('activity_categories')

@login_required
def create_match(request, profile_id):
    profile_to_match = get_object_or_404(Profile, id=profile_id)
    match, created = Match.objects.get_or_create(user1=request.user.profile, user2=profile_to_match)
    match.is_confirmed_by_user1 = True
    match.is_confirmed_by_user2 = True
    match.save()
    return redirect('activity_categories')

@login_required
def add_to_friends(request, profile_id):
    profile_to_add = get_object_or_404(Profile, id=profile_id)
    request.user.profile.add_friend(profile_to_add.user)
    return redirect('activity_categories')

@login_required
def add_like(request, profile_id):
    profile_to_like = get_object_or_404(Profile, id=profile_id)
    request.user.profile.add_like(profile_to_like.user)
    return redirect('activity_categories')

@csrf_exempt
@login_required
def update_mode(request):
    if request.method == "POST":
        night_mode = request.POST.get('night_mode') == 'true'
        profile = request.user.profile
        profile.night_mode = night_mode
        profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
@csrf_exempt
def upload_profile_crop(request):
    if request.method == "POST" and request.FILES:
        user_profile = request.user.profile  # Предполагается, что у вас есть связанная модель профиля с моделью User.
        user_profile.photo_cover = request.FILES['image']
        user_profile.save()

        # Возвращаем успешный ответ
        return JsonResponse({"success": True, "image_url": user_profile.photo_cover.url})
    
    return JsonResponse({"success": False, "message": "Invalid request."})


@login_required
def add_friend(request, user_id):
    user_to_add = get_object_or_404(User, id=user_id)
    user = request.user
    profile = get_object_or_404(Profile, user=request.user)
    try:
        profile.add_friend(user_to_add.profile)
        channel_layer = get_channel_layer()
        
        avatar_url = user.profile.photo.url if user.profile.photo else static(
            'images/affect.jpg')
        async_to_sync(channel_layer.group_send)(f"user_{user_to_add.id}", {
            'type': 'send_notification',
            'message': f"The user added you as a friend.",
            'recipient_id': user_to_add.id,
            'notification_type': 'other',
            'sender_name': user.get_full_name() or user.username,
            'sender_avatar_url': avatar_url,
        })
        
           
        messages.success(request, 'Successfully added as a friend.')
    except Exception as e:
        messages.error(request, str(e))
    
    
    return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))

@login_required
def remove_friend(request, user_id):
    user_to_remove = get_object_or_404(User, id=user_id)
    user = request.user
    profile = get_object_or_404(Profile, user=request.user)
    try:
        profile.remove_friend(user_to_remove.profile)

        channel_layer = get_channel_layer()
        
        avatar_url = user.profile.photo.url if user.profile.photo else static(
            'images/affect.jpg')
        async_to_sync(channel_layer.group_send)(f"user_{user_to_remove.id}", {
            'type': 'send_notification',
            'message': f"The user remove you as a friend.",
            'recipient_id': user_to_remove.id,
            'notification_type': 'other',
            'sender_name': user.get_full_name() or user.username,
            'sender_avatar_url': avatar_url,
        })
        messages.success(request, 'Successfully removed from friends.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    try:
        profile.follow(user_to_follow.profile)
        messages.success(request, 'Successfully subscribed.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))

@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    try:
        profile.unfollow(user_to_unfollow.profile)
        messages.success(request, 'Successfully unsubscribed.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))


@login_required
def birthdays(request):
    # Получаем друзей текущего пользователя
    friends = request.user.profile.friends.all()

    # Фильтруем друзей по сегодняшней дате рождения
    todays_birthdays = friends.filter(date_of_birth__month=date.today().month,
                                      date_of_birth__day=date.today().day)
    current_month = date.today().month
    current_day = date.today().day

    # Если хотите исключить уже прошедшие дни рождения в этом месяце:
    upcoming_birthdays = friends.filter(date_of_birth__month=current_month, date_of_birth__day__gt=current_day).order_by('date_of_birth__day')


    context = {
        'todays_birthdays': todays_birthdays,
        'upcoming_birthdays': upcoming_birthdays
    }
  
    return render(request, 'account/birthdays.html', context)


def get_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def add_to_favorites(request, username, status_id):
    user = get_object_or_404(User, username=username)
    status = get_object_or_404(Status, id=status_id)

    if not request.user.favorite_statuses.filter(id=status_id).exists():
        StatusFavorite.objects.create(user=request.user, status=status)

    return JsonResponse({'success': True})


def remove_from_favorites(request, username, status_id):
    user = get_object_or_404(User, username=username)
    status = get_object_or_404(Status, id=status_id)

    try:
        favorite_entry = StatusFavorite.objects.get(
            user=request.user, status=status)
        favorite_entry.delete()
        success = True
    except StatusFavorite.DoesNotExist:
        success = False

    return JsonResponse({'success': success})



def search_friends(request):
    search_query = request.GET.get('search_query', '')
    

    # Разделение введенного запроса на имя и фамилию
    names = search_query.split(' ')
    first_name = names[0] if names else ''
    last_name = names[1] if len(names) > 1 else ''

    # Используем Q-объект для выполнения поиска по имени и фамилии
    results = User.objects.filter(
        Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
    )
    

    results_list = [{'name': f"{profile.first_name} {profile.last_name}",
                     'avatar_url': profile.profile.photo.url if profile.profile.photo else static(
                         'images/affect.jpg'),
                     'user_url': reverse('user_detail', args=[profile.username])} for profile in results]
    

    return JsonResponse({'results': results_list, 'search_query': search_query})
