# Generated by Django 4.2 on 2023-09-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_remove_status_followers_remove_status_friends_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following_set', to='account.profile'),
        ),
    ]
