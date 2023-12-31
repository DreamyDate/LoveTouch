# Generated by Django 4.2 on 2023-09-16 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_delete_userlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='reason_for_blocking',
            field=models.TextField(blank=True, null=True),
        ),
    ]
