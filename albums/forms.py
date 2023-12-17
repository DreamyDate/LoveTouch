from django import forms
from .models import Album, Photo, Comment, Like
from django.forms import Textarea
from django.core.exceptions import ValidationError


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_photo']
        widgets = {
            'description': Textarea(attrs={'rows': 5, 'cols': 30}),
        }

class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # извлекаем переданного пользователя
        super(PhotoForm, self).__init__(*args, **kwargs)
        if user:  # если пользователь передан, фильтруем альбомы
            self.fields['album'].queryset = Album.objects.filter(user=user)
    
    def clean_album(self):
        album = self.cleaned_data.get('album')
        if not album:
            raise ValidationError('Please select or create an album.')
        return album
    
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'description': Textarea(attrs={'rows': 4, 'cols': 30}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []

