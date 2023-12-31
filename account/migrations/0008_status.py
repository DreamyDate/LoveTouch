# Generated by Django 4.2 on 2023-08-06 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_alter_profile_language_alter_profile_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('type', models.CharField(choices=[('text', 'Text'), ('photo', 'Photo'), ('video', 'Video')], max_length=5)),
                ('expiration_date', models.DateTimeField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='status_photos/users/%Y/%m/%d/')),
                ('video', models.FileField(blank=True, null=True, upload_to='status_videos/users/%Y/%m/%d/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
