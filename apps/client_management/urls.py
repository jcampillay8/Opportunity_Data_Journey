from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_management_home, name="client_management_home"),
]