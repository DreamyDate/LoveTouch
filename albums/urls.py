from django.urls import path
from . import views
from .views import (
    AlbumListView, AlbumEditView, AlbumDeleteView, PhotoUpdateView, PhotoDeleteAjaxView, PhotoDetailView,  # добавьте эту строку
    CommentCreateView
)



urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    
    path('albums/edit/<int:pk>/', AlbumEditView.as_view(), name='album_edit'),
    path('album/delete/<int:pk>/', AlbumDeleteView.as_view(), name='album_delete'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/update/<int:pk>/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('delete_photo/', PhotoDeleteAjaxView.as_view(), name='delete_photo'),
    path('api/photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('photo/<int:photo_id>/toggle_comments_photo/', views.toggle_comments, name='toggle_comments_photo'),
    path('photo/<int:photo_id>/all_comments/', AlbumListView.as_view(), name='all_comments'),
    path('toggle_favorite/<int:photo_id>/', views.toggle_favorite, name='toggle_favorite'),

]

