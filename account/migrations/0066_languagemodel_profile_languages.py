# Generated by Django 4.2 on 2023-12-04 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0065_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(blank=True, to='account.languagemodel'),
        ),
    ]
