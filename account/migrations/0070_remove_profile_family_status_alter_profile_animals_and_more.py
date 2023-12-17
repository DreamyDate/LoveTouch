# Generated by Django 4.2 on 2023-12-04 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0069_alter_profile_education_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='family_status',
        ),
        migrations.AlterField(
            model_name='profile',
            name='animals',
            field=models.CharField(blank=True, choices=[('C', 'Cat/cats'), ('D', 'Dog/dogs'), ('CD', 'Cats and dogs'), ('O', 'other animals'), ('N', 'No animals')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='personality_type',
            field=models.CharField(blank=True, choices=[('I', 'Introvert'), ('E', 'Extrovert')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='religion',
            field=models.CharField(blank=True, choices=[('Ag', 'Agnosticism'), ('At', 'Atheism'), ('Bu', 'Buddhism'), ('Ca', 'Catholicism'), ('Ch', 'Christianity'), ('H', 'Hinduism'), ('Ja', 'Jainism'), ('JU', 'Judaism'), ('M', 'Mormonism'), ('I', 'Islam'), ('Z', 'Zoroastrianism'), ('Si', 'Sikhism'), ('Sp', 'Spiritualism')], max_length=255, null=True),
        ),
    ]