# Generated by Django 4.2 on 2023-09-28 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_alter_reaction_reaction_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
