from django.contrib import admin
from .models import GiftCategory, GiftItem, GiftPurchase

@admin.register(GiftCategory)
class GiftCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

@admin.register(GiftItem)
class GiftItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')

@admin.register(GiftPurchase)
class GiftPurchaseAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'recipient', 'gift_item', 'purchase_date')
