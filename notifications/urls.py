from django.urls import path
from . import views

urlpatterns = [

   path('read_notification/<int:notification_id>/', views.read_notification, name='read_notification'),
   path('read_all/', views.read_all_notifications, name='read_all_notifications'),
]
