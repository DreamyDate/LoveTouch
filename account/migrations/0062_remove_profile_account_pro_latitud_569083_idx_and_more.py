# Generated by Django 4.2 on 2023-10-22 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0061_alter_profile_photo'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='profile',
            name='account_pro_latitud_569083_idx',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='longitude',
        ),
    ]
