from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import (View, TemplateView)
from django.contrib.auth.decorators import login_required
#from .forms.request_form_dash import RequestForm
from apps.request.forms.request_form_dash import app
from django.contrib.auth import logout
from apps.utils import get_context

# Create your views here.
def client_management_home(request):
    return render(request, 'client_management/client_management_home.html')