# Generated by Django 4.2 on 2023-09-26 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0052_profile_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_superuser',
        ),
    ]
