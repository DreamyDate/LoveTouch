from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from ckeditor.fields import RichTextField

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    header_image = models.ImageField(upload_to='news/header_images/', null=True, blank=True, verbose_name='Header Image')  # Изображение для шапки записи
    show_header = models.BooleanField(default=True, verbose_name='Show Header')
    header_color = models.CharField(max_length=7, default='#FFFFFF', verbose_name='Header Color if No Image')
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug])
    
class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


