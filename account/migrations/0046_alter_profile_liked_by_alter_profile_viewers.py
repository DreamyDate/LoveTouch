# Generated by Django 4.2 on 2023-09-19 03:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0045_alter_profile_friends_alter_profile_liked_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_profiles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='viewers',
            field=models.ManyToManyField(blank=True, related_name='viewed_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
