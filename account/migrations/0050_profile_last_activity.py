# Generated by Django 4.2 on 2023-09-23 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0049_menuitem_icon_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
