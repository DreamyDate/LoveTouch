# Generated by Django 4.2 on 2023-08-10 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0015_rename_comment_status_statuscomment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='likes_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.CreateModel(
            name='StatusLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='account.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='statuslike',
            index=models.Index(fields=['user', '-created_date'], name='account_sta_user_id_06598a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='statuslike',
            unique_together={('user', 'status')},
        ),
    ]
