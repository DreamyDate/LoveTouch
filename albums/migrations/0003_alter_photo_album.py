# Generated by Django 4.2 on 2023-08-03 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_comment_like_rename_date_added_album_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='albums.album'),
        ),
    ]
