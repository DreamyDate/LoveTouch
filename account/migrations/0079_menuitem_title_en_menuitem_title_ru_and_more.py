# Generated by Django 4.2 on 2023-12-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0078_remove_menuitem_title_en_remove_menuitem_title_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='title_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='title_ua',
            field=models.CharField(max_length=50, null=True, verbose_name='Title'),
        ),
    ]