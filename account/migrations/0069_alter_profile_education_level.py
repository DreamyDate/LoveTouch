# Generated by Django 4.2 on 2023-12-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0068_alter_profile_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='education_level',
            field=models.CharField(blank=True, choices=[('A', 'Average'), ('H', 'Higher'), ('Ia', "I am studying for a master's degree"), ('Is', 'I study in college'), ('B', 'Bachelor')], max_length=2, null=True),
        ),
    ]
