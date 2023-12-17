from django.contrib import admin
from .models import Album, Photo, Comment, Like, Favorite

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at',)
    search_fields = ('title', 'description',)
    list_filter = ('created_at', 'user',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'user', 'created_at', 'comments_enabled',)
    search_fields = ('title', 'description',)
    list_filter = ('created_at', 'user', 'comments_enabled',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'photo', 'user', 'created_at', 'updated', 'active',)
    search_fields = ('text', 'user__username',)
    list_filter = ('created_at', 'updated', 'active',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo',)
    search_fields = ('user__username', 'photo__title',)
    
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo',)
    search_fields = ('user__username', 'photo__title',)
