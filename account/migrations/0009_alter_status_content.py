# Generated by Django 4.2 on 2023-08-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='content',
            field=models.TextField(max_length=200),
        ),
    ]
