# Generated by Django 4.2 on 2023-09-16 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_profile_latitude_profile_longitude'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserLocation',
        ),
    ]
