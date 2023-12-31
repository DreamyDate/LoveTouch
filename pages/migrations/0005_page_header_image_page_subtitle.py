# Generated by Django 4.2 on 2023-09-09 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_page_show_in_footer'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='pages/header_images/', verbose_name='Header Image'),
        ),
        migrations.AddField(
            model_name='page',
            name='subtitle',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Subtitle'),
        ),
    ]
