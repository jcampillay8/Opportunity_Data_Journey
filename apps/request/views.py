from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView)
from .forms.request_form import RequestForm
from django.contrib.auth import logout
from apps.utils import get_context

# Create your views here.
def request_home(request):
    return render(request, 'request/request_home.html')

def new_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = RequestForm()
    return render(request, 'request/new_request.html', {'current_page': 'request_home','form': form,'selected_language':get_context(request)})

def request_history(request):
    return render(request, 'request/request_history.html',{'current_page': 'request_home','selected_language':get_context(request)})

def request_status(request):
    return render(request, 'request/request_status.html',{'current_page': 'request_home','selected_language':get_context(request)})
