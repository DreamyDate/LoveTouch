# Generated by Django 4.2 on 2023-09-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_menuitem_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
