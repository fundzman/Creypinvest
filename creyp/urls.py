from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import index, referral_view, dashboard_denial_view

# handling the 404 error
handler404 = 'core.views.error_404_view'

urlpatterns = [
    path('', index, name="home"),
    path('r/<str:username>/', referral_view, name="refer"),
    path('dashboard/@error/@type/@user/can-not-access-dashboard/@except/profile?e=you+can+only+access+profile',
         dashboard_denial_view, name="dashboard-denial"),
    path('admin/', admin.site.urls),
    path('@admin/', include('site_admin.urls')),
    path('site/', include('core.urls')),
    path('auth/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('auth/account/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
