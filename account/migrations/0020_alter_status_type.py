# Generated by Django 4.2 on 2023-08-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_userlocation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='type',
            field=models.CharField(blank=True, choices=[('text', 'Text'), ('photo', 'Photo'), ('video', 'Video')], max_length=5, null=True),
        ),
    ]
