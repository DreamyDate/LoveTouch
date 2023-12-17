from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from . import views


urlpatterns = [

    path('', views.match_view, name='match_view'),
    path('confirm_match/<int:match_id>/', views.confirm_match, name='confirm_match'),
    path('reject_match/<int:match_id>/', views.reject_match, name='reject_match'),
    path('send-match-request/<int:user2_id>/', views.send_match_request, name="send_match_request"),
    path('filter/', views.filter_results, name='filter_results'),
    path('like/<int:user_id>/', views.add_like, name='add_like'),
    path('unlike/<int:user_id>', views.remove_like, name='remove_like'),
    path('search_people/', views.search_people, name='search_people'),
]

