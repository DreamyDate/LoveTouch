# Generated by Django 4.2 on 2023-10-22 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gift', '0002_giftcategory_giftitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]