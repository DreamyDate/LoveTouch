from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('password_change/', views.password_change, name='password_change'),
    
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('users/<username>/add_to_favorites/<int:status_id>/',
         views.add_to_favorites, name='add_to_favorites'),
    path('add_to_favorites/<int:status_id>/',
         views.add_to_favorites, name='add_to_favorites'),
    path('users/<username>/remove_from_favorites/<int:status_id>/',
         views.remove_from_favorites, name='remove_from_favorites'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('add_status/', views.add_status, name='add_status'),
    path('like_status/<int:status_id>/', views.update_like_status, name='update_like_status'),
    path('get_comments/<int:status_id>/', views.get_comments, name='get_comments_for_status'),
    path('status/<int:status_id>/delete/', views.delete_status, name='delete_status'),
    path('toggle_comments/<int:status_id>/', views.toggle_comments, name='toggle_comments'),
    path('edit-status/<int:status_id>/', views.edit_status, name='edit_status'),
    
    path('purchase_credits/', views.purchase_credits, name='purchase_credits'),
    path('premium-packages/', views.list_premium_packages, name='list_premium_packages'),
    path('buy-premium-package/<int:package_id>/', views.buy_premium_package, name='buy_premium_package'),
    path('likes/', views.activity_categories, name='likes_user'),
    path('add_to_friends/<int:profile_id>/', views.add_to_friends, name='add_to_friends'),
    path('add_like/<int:profile_id>/', views.add_like, name='add_like'),
    path('update_mode/', views.update_mode, name='update_mode'),

    path('path_to_crop_image_view/', views.upload_profile_crop, name='upload_crop'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('birthdays/', views.birthdays, name='birthdays'),
    path('edit/get_cities/', views.get_cities, name='get_cities'),
    path('search/', views.search_friends, name='search_friends'),

]
