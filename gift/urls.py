from django.urls import path
from . import views

urlpatterns = [
    # ... ваш код ...
    path('gift_shop/', views.gift_shop, name='gift_shop'),
    path('buy_gift/<int:gift_id>/', views.buy_gift, name='buy_gift'),
    path('gift_purchase_success/', views.gift_purchase_success, name='gift_purchase_success'),
]
