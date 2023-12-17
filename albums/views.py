from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Album, Photo, Comment, Like,Favorite
from .forms import AlbumForm, PhotoForm, CommentForm
from django.db.models import Q
from .forms import CommentForm  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Count
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from notifications.models import Notification


def is_ajax_request(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

class AlbumListView(LoginRequiredMixin, View):
    template_name = 'albums/album_list.html'
    album_form_class = AlbumForm
    photo_form_class = PhotoForm
   
    def get(self, request, *args, **kwargs):
        if 'photo_id' in kwargs:
            return self.get_all_comments(request, kwargs['photo_id'])

        albums = Album.objects.filter(user=request.user).prefetch_related(
            'photos',
            'photos__comments',
            'photos__likes'
        ).order_by('-created_at')
        
        latest_5_albums = albums[:5]
        
        photos = Photo.objects.filter(user=request.user, album__in=albums).annotate(
            comments_count=Count('comments', distinct=True),
            likes_count=Count('likes', distinct=True)
        )
        photo_count = Photo.objects.filter(user=request.user).count()

        album_form = AlbumForm()
        photo_form = PhotoForm(user=request.user)
        
        context = {
            'albums': albums,
            'latest_5_albums': latest_5_albums,
            'album_form': album_form,
            'photo_form': photo_form,
            'photos': photos,
            'photo_count': photo_count,
            
        }
        return render(request, self.template_name, context)
       
    def get_all_comments(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
    
        # Получаем лимит из запроса
        limit = request.GET.get('limit')
        if limit:
            comments = photo.comments.select_related('user').all().order_by('-created_at')[:int(limit)]
        else:
            comments = photo.comments.select_related('user').all().order_by('-created_at')
    
        comments_data = []
        for comment in comments:
            comment_data = {
            "text": comment.text,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "user__username": comment.user.username,
            "user__photo": comment.user.profile.photo.url
            }
            comments_data.append(comment_data)
    
        return JsonResponse({'comments': comments_data})



    def post(self, request, *args, **kwargs):
        if 'create_album' in request.POST:
            return self._handle_album_post(request)
        elif 'add_photo' in request.POST:
            return self._handle_photo_post(request)
       
    def _handle_album_post(self, request):
        album_form = self.album_form_class(request.POST, request.FILES)
        if album_form.is_valid():
            album = album_form.save(commit=False)
            album.user = request.user
            album.save()
            if is_ajax_request(request):
                return JsonResponse({"success": True, "album_id": album.pk})
            return redirect(self.get_success_url())

        context = {
            'albums': Album.objects.filter(user=request.user),
            'album_form': album_form,
            'photo_form': self.photo_form_class()
        }

        if is_ajax_request(request):
            return JsonResponse({"success": False, "errors": album_form.errors})

        return render(request, self.template_name, context)

    def _handle_photo_post(self, request):
        photo_form = self.photo_form_class(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.user = request.user
            photo.save()
            if is_ajax_request(request):
                return JsonResponse({"success": True, "photo_id": photo.pk})
            return redirect(self.get_success_url())
        else:
            # Если у нас есть ошибка в поле album
            if 'album' in photo_form.errors:
                messages.error(request, "Please select or create an album before uploading a photo.")
                return redirect('album_list')
        
        context = {
            'albums': Album.objects.filter(user=request.user),
            'album_form': self.album_form_class(),
            'photo_form': photo_form
        }

        if is_ajax_request(request):
            return JsonResponse({"success": False, "errors": photo_form.errors})

        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('album_list')

class AlbumEditView(UpdateView):
    model = Album
    fields = ['title', 'description', 'cover_photo']

    def form_valid(self, form):
        album = form.save()
        data = {
        'status': 'success',
        'message': 'Album successfully updated!',
        'album': {
            'id': album.id,
            'title': album.title,
            'description': album.description,
            'cover_photo_id': album.cover_photo.id if album.cover_photo else None
        }
    }
        return JsonResponse(data)


    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

class AlbumDeleteView(View):
    def post(self, request, *args, **kwargs):
        album_id = request.POST.get('album_id')
        album = get_object_or_404(Album, pk=album_id)

        # Убедитесь, что у пользователя есть права на удаление (если это необходимо)
        if request.user != album.user:
            return JsonResponse({"success": False, "error": "No permission to delete the album."}, status=403)

        album.delete()
        return JsonResponse({"success": True}, status=200)

class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'albums/photo/photo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = get_object_or_404(Photo, id=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(photo=self.object).order_by('-created_at')
        context['form'] = CommentForm()  # добавляем форму комментариев в контекст
        context['likes_count'] = self.object.likes.count()
        context['comments_enabled'] = self.object.comments_enabled

        # Проверяем, лайкнул ли пользователь эту фотографию или нет
       
        context['is_liked'] = self.object.likes.filter(user=self.request.user).exists()
        return context

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_success_url(self):
        messages.success(self.request, "Фотография успешно обновлена!")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "При редактировании фотографии произошла ошибка.")
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Если AJAX запрос
        if request.is_ajax():
            if self.object:  # если объект успешно обновлен
                return JsonResponse({
                    'status': 'success',
                    'message': 'Фотография успешно обновлена!',
                    'photo': {
                        'id': self.object.id,
                        'title': self.object.title,
                        'description': self.object.description,
                        'url': self.object.image.url  # предполагая, что у модели Photo есть поле image
                    }
                })
            else:
                errors = []
                for field, error_list in form.errors.items():
                    errors.extend(error_list)
                return JsonResponse({
                    'status': 'error',
                    'message': ' '.join(errors)
                })

        return response


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'albums/comment_form.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.photo = get_object_or_404(Photo, id=self.kwargs['pk'])
        comment.save()
        user_profile_photo_url = comment.user.profile.photo.url if comment.user.profile.photo else static('images/affect.jpg')
        # Если форма действительна и комментарий добавлен, отправьте положительный ответ.
        data = {
        'message': 'Комментарий успешно добавлен!',
        'comment_data': {
            'text': comment.text,
            'user_full_name': comment.user.get_full_name(),
            'user_profile_photo': user_profile_photo_url,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
        return JsonResponse(data)

    def form_invalid(self, form):
        # Если возникли ошибки, отправьте их.
        return JsonResponse({'errors': form.errors}, status=400)

@login_required
@csrf_exempt
def like_photo(request, photo_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        like, created = Like.objects.get_or_create(user=request.user, photo=photo)

        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True

        last_3_users = photo.likes.order_by('-id')[:3].values_list('user__username', flat=True)

        return JsonResponse({
            'likes_count': photo.likes.count(),
            'is_liked': is_liked,
            'last_3_users': list(last_3_users)
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

def set_cover(self, photo):
    if photo.album == self:
        self.cover_photo = photo
        self.save()
    else:
        raise ValueError("Фотография не принадлежит этому альбому.")
    
class PhotoDeleteAjaxView(View):

    def post(self, request, *args, **kwargs):
        photo_id = request.POST.get('photo_id')
        
        try:
            photo = Photo.objects.get(id=photo_id, user=request.user)
            photo.delete()
            
            # Подсчет общего количества фотографий после удаления
            total_photos = Photo.objects.filter(user=request.user).count()
            
            return JsonResponse({"success": True, "total_photos": total_photos})
        except Photo.DoesNotExist:
            return JsonResponse({"success": False, "error": "Photo not found or not owned by user."})

@login_required
def toggle_comments(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    # Убедимся, что текущий пользователь имеет право менять настройки этой фотографии
    if request.user != photo.user:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    photo.comments_enabled = not photo.comments_enabled
    photo.save()

    message = "Комментарии отключены." if not photo.comments_enabled else "Комментарии включены."
    messages.success(request, message)

    return redirect('photo_detail', pk=photo_id)



@login_required
def toggle_favorite(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    # Проверка на наличие избранного
    favorite, created = Favorite.objects.get_or_create(user=request.user, photo=photo)

    if created:
        action = "added"
    else:
        favorite.delete()
        action = "removed"

    return JsonResponse({'action': action, 'photo_id': photo_id})
