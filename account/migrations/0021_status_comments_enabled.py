# Generated by Django 4.2 on 2023-09-05 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_status_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='comments_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
