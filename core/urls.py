from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from apps.Error_Handler.views import Error404View, Error505View

urlpatterns = [
    path("", include("apps.home.urls")),
    path("authentication/", include("apps.authentication.urls")),
    path("request/", include("apps.request.urls")),
    path('contact/',include("apps.contact.urls")),
    path('client_management/',include("apps.client_management.urls")),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path("admin/", admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)

handler404 = Error404View.as_view()
handler505 = Error505View.as_error_view()