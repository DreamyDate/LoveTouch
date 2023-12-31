# Generated by Django 4.2 on 2023-09-16 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_profile_is_blocked_profile_reason_for_blocking'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('date_blocked', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='credits',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
