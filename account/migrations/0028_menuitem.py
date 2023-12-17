# Generated by Django 4.2 on 2023-09-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_delete_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('icon_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
