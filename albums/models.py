from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_photo = models.ForeignKey('Photo', related_name='cover_for', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title

class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)  # Теперь это поле необязательно
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/users/%Y/%m/%d/', default='photos/no_image.jpg')
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE, blank=True, null=True)  # Теперь это поле необязательно
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comments_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    def liked_by_current_user(self, user):
        return self.likes.filter(user=user).exists()
    
    def has_more_than_five_comments(self):
        return self.comments.count() > 5
    
    def get_last_five_comments(self):
        return self.comments.all().order_by('-created_at')[:5]
    def is_favorite_for_user(self, user):
        return self.favorites.filter(user=user).exists()


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at']),]

    def __str__(self):
        return f'Comment by {self.user.username} on photo ID {self.photo.id}'

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ForeignKey(Photo, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'photo',)

    def __str__(self):
        return f'{self.user.username} likes {self.photo.title}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'photo',)

    def __str__(self):
        return f'{self.user.username} added {self.photo.title} to favorites'
