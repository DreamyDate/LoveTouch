# Generated by Django 4.2 on 2023-09-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_alter_statuscomment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
