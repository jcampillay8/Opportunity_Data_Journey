from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.home.urls")),
    path("authentication/", include("apps.authentication.urls")),
    path("request/", include("apps.request.urls")),
    path('contact/',include("apps.contact.urls")),
    path('client_management/',include("apps.client_management.urls")),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path("admin/", admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
