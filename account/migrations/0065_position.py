# Generated by Django 4.2 on 2023-12-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0064_profile_animals_profile_children_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
