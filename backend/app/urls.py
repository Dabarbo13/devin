from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/clinical-trials/', include('clinical_trials.urls')),
    path('api/donation-management/', include('donation_management.urls')),
    path('api/recruiting/', include('recruiting.urls')),
    path('api/sponsor-portal/', include('sponsor_portal.urls')),
    path('api/web-store/', include('web_store.urls')),
    path('healthz/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
