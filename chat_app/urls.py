from django.urls import path
from . import views
from . import consumers  # Добавьте этот импорт
app_name = 'chat'

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('<int:room_id>/', views.chat_detail, name='chat_detail'),
    path('<int:chat_id>/ws/', views.chat_ws, name='chat_ws'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('delete_chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('latest_chats/', views.latest_chats, name='latest_chats'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),


]
