from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", views.request_home, name="request_home"),
    #path("new_request", views.new_request, name="new_request"),
    path("new_request/<int:pk>", views.new_request, name="new_request"),
    path('request_history/', views.request_history, name='request_history'),
    path('request_status', views.request_status, name="request_status"),
    path('revision_solicitud', views.revision_solicitud, name="revision_solicitud"),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)