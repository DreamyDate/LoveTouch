# Generated by Django 4.2 on 2023-10-01 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0060_profile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/'),
        ),
    ]