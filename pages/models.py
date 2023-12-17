from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Page(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, verbose_name='Subtitle', blank=True, null=True)  # Подзаголовок
    content = RichTextField()
    slug = models.SlugField(unique=True, max_length=100)
    show_in_footer = models.BooleanField(default=False, verbose_name='Show in footer menu')
    header_image = models.ImageField(upload_to='pages/header_images/', null=True, blank=True, verbose_name='Header Image')  # Изображение для шапки записи
    show_header = models.BooleanField(default=True, verbose_name='Show Header')
    header_color = models.CharField(max_length=7, default='#FFFFFF', verbose_name='Header Color if No Image')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', args=[self.slug])


