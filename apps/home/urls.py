from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", views.welcome, name="welcome"),
    path("home", views.home, name="home"),
    path('contact_home', views.contact_home, name="contact_home"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)