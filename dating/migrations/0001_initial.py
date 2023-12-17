# Generated by Django 4.2 on 2023-09-16 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0031_menuitem_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('matched_on', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed_by_user1', models.BooleanField(default=False)),
                ('is_confirmed_by_user2', models.BooleanField(default=False)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_matches', to='account.profile')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_matches', to='account.profile')),
            ],
        ),
    ]
