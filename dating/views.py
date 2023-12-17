from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from account.models import Profile, PremiumPurchase, PremiumPackage
from .models import Match
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from pusher import Pusher
from django.conf import settings
from django.contrib import messages
from geopy.distance import geodesic
import random
from .forms import ProfileFilterForm
from django.shortcuts import get_object_or_404
from cities_light.models import City
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from collections import defaultdict


def get_candidates_in_zone(profile, distance_km=100):
    user_city = profile.city

    if user_city:
        user_coordinates = (user_city.latitude, user_city.longitude)

        candidates_in_zone = []

        # Получение всех профилей, у которых заполнено поле города
        all_candidates = Profile.objects.exclude(
            id=profile.id).exclude(city__isnull=True)

        for candidate in all_candidates:
            candidate_city = candidate.city

            if candidate_city and candidate_city.latitude and candidate_city.longitude:
                candidate_coords = (candidate_city.latitude,
                                    candidate_city.longitude)
                distance = geodesic(
                    user_coordinates, candidate_coords).kilometers

                if distance <= distance_km:
                    candidates_in_zone.append(candidate)

        return candidates_in_zone
    else:
        # Обработка ситуации, если у профиля нет указанного города
        return []


def get_top_matches(user_profile, top_n=10):
    # Получите всех потенциальных кандидатов
    potential_matches = Profile.objects.exclude(id=user_profile.id).exclude(
        friends=user_profile).exclude(followers=user_profile)

    premium_candidates = []

    for candidate in potential_matches:
        if PremiumPurchase.objects.filter(profile=candidate).exists() and candidate.is_premium_active():
            if not (user_profile.friends.filter(id=candidate.id).exists() or user_profile.followers.filter(id=candidate.id).exists()):
                premium_candidates.append(candidate)

    # Выберите случайное количество пользователей из списка кандидатов с премиум-аккаунтами (не более чем top_n)
    selected_matches = random.sample(
        premium_candidates, min(len(premium_candidates), top_n))

    return selected_matches


@login_required
def find_matches_for_user(profile, top_n=5):
    friends_ids = [friend.id for friend in profile.friends.all()]
    followers_ids = [follower.id for follower in profile.followers.all()]

    potential_matches = Profile.objects.exclude(id=profile.id).exclude(
        id__in=friends_ids).exclude(id__in=followers_ids)

    scored_matches = []
    for candidate in potential_matches:
        score = 0

        # Местоположение
        if profile.city == candidate.city:
            score += 20

        # Цели отношений
        if profile.relationship_goals == candidate.relationship_goals:
            score += 50

        # Внешность
        if profile.hair_color == candidate.hair_color:
            score += 5
        if profile.eye_color == candidate.eye_color:
            score += 5
        if profile.physique == candidate.physique:
            score += 10

        # Привычки
        if profile.smoking == candidate.smoking:
            score += 10
        if profile.alcohol == candidate.alcohol:
            score += 10

        # Другие характеристики
        if profile.tatu == candidate.tatu:
            score += 5
        if profile.piercing == candidate.piercing:
            score += 5
        if profile.scars == candidate.scars:
            score += 5

        # Проверьте совпадение по возрасту, росту и весу
        if profile.age and candidate.age:
            age_difference = abs(candidate.age - profile.age)
            if age_difference <= 5:  # 5 лет разницы
                score += 10

        if profile.height and candidate.height:
            height_difference = abs(profile.height - candidate.height)
            if height_difference <= 10:  # 10 см разницы
                score += 5

        weight_difference = abs(
            float(profile.weight or 0) - float(candidate.weight or 0))
        if weight_difference <= 5:  # 5 кг разницы
            score += 5

        # Пол
        if profile.gender != candidate.gender:
            score += 10  # Можно модифицировать это число в зависимости от ваших требований

        # Добавляем новые критерии из модели профиля
        if profile.zodiac_sign == candidate.zodiac_sign:
            score += 15

        if profile.sexual_orientation == candidate.sexual_orientation:
            score += 15

        if profile.relationship_status == candidate.relationship_status:
            score += 15

        if profile.education_level == candidate.education_level:
            score += 15

        if profile.personality_type == candidate.personality_type:
            score += 15

        if profile.work_and_education == candidate.work_and_education:
            score += 15

        if profile.animals == candidate.animals:
            score += 15

        if profile.children == candidate.children:
            score += 15

        if profile.religion == candidate.religion:
            score += 15

        # Другие критерии можно добавить по аналогии

        scored_matches.append((candidate, score))

    # Сортируйте и фильтруйте кандидатов на основе оценок
    sorted_matches = sorted(scored_matches, key=lambda x: x[1], reverse=True)
    best_matches = [match[0] for match in sorted_matches if match[1] >= 10]

    # Получите "топ знакомства"
    top_matches = get_top_matches(profile, top_n)

    # Получите кандидатов из +100 км зоны
    candidates_in_zone = get_candidates_in_zone(profile)

    # Объедините все кандидаты и удалите дубликаты
    all_candidates = best_matches + candidates_in_zone
    all_candidates = list(set(all_candidates))

    # Если количество кандидатов превышает top_n, выберите случайные top_n из них
    if len(all_candidates) > top_n:
        all_candidates = random.sample(all_candidates, top_n)
        all_candidates.extend(top_matches)

    # Удаление дубликатов
    seen = defaultdict(int)
    unique_candidates = []
    for candidate in all_candidates:
        if seen[candidate] == 0:
            unique_candidates.append(candidate)
            seen[candidate] = 1

    return unique_candidates


@login_required
def match_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    matches = find_matches_for_user(user_profile)

    confirmed_matches = Match.objects.filter(
        Q(user1=user_profile, is_confirmed_by_user1=True, is_confirmed_by_user2=True) |
        Q(user2=user_profile, is_confirmed_by_user1=True, is_confirmed_by_user2=True)
    )

    unmatched_matches = [
        match for match in matches
        if not confirmed_matches.filter(Q(user1=user_profile, user2=match) | Q(user1=match, user2=user_profile)).exists()
        and not Match.objects.filter(Q(user1=match, user2=user_profile) | Q(user1=user_profile, user2=match)).exists()
    ]

    pending_matches = Match.objects.filter(
        Q(user1=user_profile, is_confirmed_by_user1=False) |
        Q(user2=user_profile, is_confirmed_by_user2=False)
    )

    context = {
        'matches': unmatched_matches,
        'pending_matches': pending_matches,

    }

    return render(request, 'matches.html', context)


@login_required
def confirm_match(request, match_id):
    match = Match.objects.get(id=match_id)

    if request.user.profile == match.user1:
        match.is_confirmed_by_user1 = True
    elif request.user.profile == match.user2:
        match.is_confirmed_by_user2 = True
        match.is_confirmed_by_user1 = True

    match.save()

    return redirect('match_view')


@login_required
def reject_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        if request.user.profile in [match.user1, match.user2]:
            match.delete()
            return redirect('match_view')
    except Match.DoesNotExist:
        messages.error(request, 'Ошибка при удалении совпадения!')

    return redirect('match_view')


@login_required
def send_match_request(request, user2_id):
    user1 = request.user  # это уже объект User
    user2 = get_object_or_404(User, pk=user2_id)

    # Проверка, чтобы не создать матч с самим собой
    if user1 == user2:
        messages.error(request, "You can't create a match with yourself")

    match, created = Match.objects.get_or_create(
        user1=user1.profile,  # здесь мы берем профиль из объекта User
        user2=user2.profile,  # и здесь также
        defaults={'score': 0}  # начальное значение для поля score
    )

    avatar_url = get_user_avatar_url(user1.id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"user_{user2.id}", {
        'type': 'send_notification',
        'message': f"User '{user1.get_full_name()}' sent you a request for dating",
        'recipient_id': user2.id,
        'notification_type': 'acquaintance',
        'sender_name': user1.get_full_name() or user1.username,
        'sender_avatar_url': avatar_url,
    })

    # Если матч уже существует, обработайте это соответствующим образом.
    if not created:
        messages.error(request, "Match request already exists.")
        return redirect('match_view')

    messages.success(request, "Match request sent successfully.")
    return redirect('match_view')


def get_user_avatar_url(user_id):
    try:
        user = User.objects.get(pk=user_id)
        if user.profile.photo:
            return user.profile.photo.url
        else:
            return "/static/images/affect.jpg"  # Замените на свой путь к аватару по умолчанию
    except User.DoesNotExist:
        return "/static/images/affect.jpg"  # Замените на свой путь к аватару по умолчанию


def filter_profiles(user_exclude=None, **kwargs):
    profiles = Profile.objects.all()
    
    if user_exclude:
        profiles = profiles.exclude(user=user_exclude)\


    
    # Фильтрация по цели знакомства
    if kwargs.get('search_goals'):
        profiles = profiles.filter(relationship_goals=kwargs['search_goals'])

   # Фильтрация по гендеру
    search_gender = kwargs.get('search_gender', [])
    if search_gender:
        profiles = profiles.filter(gender__in=search_gender)

    search_physique = kwargs.get('search_physique', [])

    if search_physique:
        profiles = profiles.filter(physique__in=search_physique)

    search_smoking = kwargs.get('search_smoking', [])
    if search_smoking:
        profiles = profiles.filter(smoking__in=search_smoking)

    search_personality_type = kwargs.get('search_personality_type', [])

    if search_personality_type:
        profiles = profiles.filter(
            personality_type__in=search_personality_type)

    search_relationship_status = kwargs.get('search_relationship_status', [])

    if search_relationship_status:
        profiles = profiles.filter(
            relationship_status__in=search_relationship_status)

    search_sexual_orientation = kwargs.get('search_sexual_orientation', [])
    if search_sexual_orientation:
        profiles = profiles.filter(
            sexual_orientation__in=search_sexual_orientation)

    search_children = kwargs.get('search_children', [])
    if search_children:
        profiles = profiles.filter(
            children__in=search_children)

    search_alcohol = kwargs.get('search_alcohol', [])
    if search_alcohol:
        profiles = profiles.filter(
            alcohol__in=search_alcohol)

    search_tatu = kwargs.get('search_tatu', [])
    if search_tatu:
        profiles = profiles.filter(
            tatu__in=search_tatu)

    search_piercing = kwargs.get('search_piercing', [])
    if search_piercing:
        profiles = profiles.filter(
            piercing__in=search_piercing)

    search_scars = kwargs.get('search_scars', [])
    if search_scars:
        profiles = profiles.filter(
            scars__in=search_scars)

    search_zodiac_sign = kwargs.get('search_zodiac_sign', [])
    if search_zodiac_sign:
        profiles = profiles.filter(
            zodiac_sign__in=search_zodiac_sign)

    search_animals = kwargs.get('search_animals', [])
    if search_animals:
        profiles = profiles.filter(
            animals__in=search_animals)

    search_religion = kwargs.get('search_religion', [])
    if search_religion:
        profiles = profiles.filter(
            religion__in=search_religion)

    search_languages = kwargs.get('search_languages', [])
    if search_languages:
        profiles = profiles.filter(
            languages__in=search_languages)

    search_education_level = kwargs.get('search_education_level', [])
    if search_education_level:
        profiles = profiles.filter(
            education_level__in=search_education_level)

    search_work_and_education = kwargs.get('search_work_and_education', [])
    if search_work_and_education:
        profiles = profiles.filter(
            work_and_education__in=search_work_and_education)

        # Фильтрация по возрасту
    min_age = kwargs.get('search_age_from')
    max_age = kwargs.get('search_age_to')
    conditions = Q()
    if min_age:
        conditions &= Q(age__gte=int(min_age))
    if max_age:
        conditions &= Q(age__lte=int(max_age))
    if conditions:
        profiles = profiles.filter(conditions)

    # Фильтрация по географическому приближению (радиус)
    if kwargs.get('search_radius_km') and kwargs.get('current_latitude') and kwargs.get('current_longitude'):
        current_latitude = kwargs.get('current_latitude')
        current_longitude = kwargs.get('current_longitude')
        radius = float(kwargs.get('search_radius_km'))

        filtered_profiles = []
        for profile in profiles:
            if profile.latitude and profile.longitude:
                distance = geodesic((current_latitude, current_longitude),
                                    (profile.latitude, profile.longitude)).kilometers
                if distance <= radius:
                    filtered_profiles.append(profile)

        profiles = Profile.objects.filter(
            id__in=[p.id for p in filtered_profiles])

    # Фильтрация по городу
    if kwargs.get('search_city'):
        profiles = profiles.filter(city=kwargs['search_city'])

    # Фильтрация по стране
    if kwargs.get('search_country'):
        profiles = profiles.filter(country=kwargs['search_country'])

    # Фильтрация по росту
    min_height = kwargs.get('search_min_height')
    max_height = kwargs.get('search_max_height')
    if min_height:
        profiles = profiles.filter(height__gte=float(min_height))
    if max_height:
        profiles = profiles.filter(height__lte=float(max_height))

    # Фильтрация по весу
    min_weight = kwargs.get('search_min_weight')
    max_weight = kwargs.get('search_max_weight')
    if min_weight:
        profiles = profiles.filter(weight__gte=float(min_weight))
    if max_weight:
        profiles = profiles.filter(weight__lte=float(max_weight))

    return profiles


def filter_results(request):
    
    # Получите параметры из GET-запроса
    search_gender = request.GET.getlist('search_gender')
    search_smoking = request.GET.getlist('search_smoking')
    search_age_from = request.GET.get('search_age_from')
    search_age_to = request.GET.get('search_age_to')
    search_goals = request.GET.get('search_goals')
    search_physique = request.GET.getlist('search_physique')
    search_personality_type = request.GET.getlist('search_personality_type')
    search_relationship_status = request.GET.getlist(
        'search_relationship_status')
    search_sexual_orientation = request.GET.getlist(
        'search_sexual_orientation')
    search_children = request.GET.getlist(
        'search_children')
    search_alcohol = request.GET.getlist(
        'search_alcohol')
    search_tatu = request.GET.getlist(
        'search_tatu')
    search_piercing = request.GET.getlist(
        'search_piercing')
    search_scars = request.GET.getlist(
        'search_scars')
    search_zodiac_sign = request.GET.getlist(
        'search_zodiac_sign')
    search_animals = request.GET.getlist(
        'search_animals')
    search_religion = request.GET.getlist(
        'search_religion')
    search_languages = request.GET.getlist(
        'search_languages')
    search_education_level = request.GET.getlist(
        'search_education_level')
    search_work_and_education = request.GET.getlist(
        'search_work_and_education')

    search_city = request.GET.get('search_city')
    search_country = request.GET.get('search_country')
    search_radius_km = request.GET.get('search_radius_km')
    current_latitude = request.GET.get('current_latitude')
    current_longitude = request.GET.get('current_longitude')
    search_min_height = request.GET.get('search_min_height')
    search_max_height = request.GET.get('search_max_height')
    search_min_weight = request.GET.get('search_min_weight')
    search_max_weight = request.GET.get('search_max_weight')

    # Используйте функцию filter_profiles для фильтрации
    profiles = filter_profiles(
        search_gender=search_gender,
        search_smoking=search_smoking,
        search_age_from=search_age_from,
        search_age_to=search_age_to,
        search_goals=search_goals,
        search_physique=search_physique,
        search_personality_type=search_personality_type,
        search_relationship_status=search_relationship_status,
        search_sexual_orientation=search_sexual_orientation,
        search_children=search_children,
        search_alcohol=search_alcohol,
        search_tatu=search_tatu,
        search_piercing=search_piercing,
        search_scars=search_scars,
        search_zodiac_sign=search_zodiac_sign,
        search_animals=search_animals,
        search_religion=search_religion,
        search_languages=search_languages,
        search_education_level=search_education_level,
        search_work_and_education=search_work_and_education,

        search_city=search_city,
        search_country=search_country,
        search_radius_km=search_radius_km,
        current_latitude=current_latitude,
        current_longitude=current_longitude,
        search_min_height=search_min_height,
        search_max_height=search_max_height,
        search_min_weight=search_min_weight,
        search_max_weight=search_max_weight,

    )
# Получите текущего пользователя
    current_user_profile = request.user.profile if request.user.is_authenticated else None

    # Получите выбранного пользователя (например, по ID из GET-запроса)
    selected_user_id = request.GET.get('selected_user_id')
    selected_user_profile = Profile.objects.get(
        pk=selected_user_id) if selected_user_id else None

    # Проверьте, является ли выбранный пользователь другом текущего пользователя
    is_friend = current_user_profile.is_friend_of(
        selected_user_profile) if current_user_profile and selected_user_profile else False
    is_following = current_user_profile.is_following_of(
        selected_user_profile) if current_user_profile and selected_user_profile else False

    return render(request, 'filter/results.html', {'profiles': profiles, 'search_gender': search_gender, 'is_friend': is_friend, 'is_following': is_following, })


def add_like(request, user_id):
    # Получаем объект профиля
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)

    # Добавляем лайк от текущего пользователя
    profile.add_like(request.user)

    return redirect(request.META['HTTP_REFERER'])


def remove_like(request, user_id):
    # Получаем объект профиля
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)

    # Удаляем лайк от текущего пользователя
    profile.remove_like(request.user)

    return redirect(request.META['HTTP_REFERER'])


def search_people(request):
    user = request.user

    current_premium_package = None
    filter_settings = None

    try:
        latest_purchase = PremiumPurchase.objects.filter(
            profile__user=user).latest('purchase_date')
        current_premium_package = latest_purchase.package
    except PremiumPurchase.DoesNotExist:
        pass

    if current_premium_package:
        filter_settings = current_premium_package.get_filter_settings()

    profiles = Profile.objects.all()

    if request.method == 'POST':
        filter_form = ProfileFilterForm(request.POST)
        if filter_form.is_valid():
            kwargs = {
                'gender': filter_form.cleaned_data['search_gender'],
                'min_age': filter_form.cleaned_data['search_age_from'],
                'max_age': filter_form.cleaned_data['search_age_to'],
                'relationship_goal': filter_form.cleaned_data['search_goals'],
                'city': filter_form.cleaned_data['search_city'],
                'country': filter_form.cleaned_data['search_country'],
                'search_radius_km': filter_form.cleaned_data['search_radius'],
                'current_latitude': filter_form.cleaned_data['current_latitude'],
                'current_longitude': filter_form.cleaned_data['current_longitude'],
            }

            # Отладочный вывод
            print("Before filtering:", profiles)

            # Исключаем текущего пользователя из результатов фильтрации
            profiles = filter_profiles(user_exclude=user, **kwargs)

            # Отладочный вывод
            print("After filtering:", profiles)

            context = {
                'filter_settings': filter_settings,
                'form': filter_form,
                'profiles': profiles,
            }

            return render(request, 'filter/search.html', context)
    else:
        filter_form = ProfileFilterForm()
    
    context = {
        'filter_settings': filter_settings,
        'form': filter_form,
        'profiles': profiles,  # Добавлено для обработки по умолчанию без фильтрации
    }

    # Исключаем текущего пользователя из результатов фильтрации
    context['user_exclude'] = user

    return render(request, 'filter/search.html', context)
