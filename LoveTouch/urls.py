from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from news.sitemaps import PostSitemap

from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
 'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('news/', include('news.urls', namespace='news')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                                            name='django.contrib.sitemaps.views.sitemap'),
    path('social-auth/',include('social_django.urls', namespace='social')),
    path('albums/', include('albums.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('dating/', include('dating.urls')),
    path('chat/', include('chat_app.urls', namespace='chat')),
    path('notifications/', include('notifications.urls')),
    path('gifts/', include('gift.urls')),
    path('rosetta/', include('rosetta.urls')),

    path('i18n/', include('django.conf.urls.i18n'))

] 

urlpatterns += i18n_patterns(
    *urlpatterns,
    prefix_default_language=False,
)

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT)
