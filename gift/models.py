from django.db import models
from django.contrib.auth.models import User

class GiftCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class GiftItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='gifts/', blank=True, null=True)
    price = models.PositiveIntegerField(help_text="Price of the gift in some virtual currency or points.")
    category = models.ForeignKey(GiftCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='gifts')
    is_new = models.BooleanField(default=False)  # Новое поле "новинка" для продуктов

    def __str__(self):
        return self.name

class GiftPurchase(models.Model):
    buyer = models.ForeignKey(User, related_name='gifts_bought', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='gifts_received', on_delete=models.CASCADE)
    gift_item = models.ForeignKey(GiftItem, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

