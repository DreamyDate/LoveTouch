# Generated by Django 4.2 on 2023-08-07 19:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_status_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
