# Generated by Django 4.2 on 2023-08-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_profile_dating_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('ru', 'Russian')], default='ru', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='timezone',
            field=models.CharField(blank=True, default='UTC', max_length=50),
        ),
    ]
