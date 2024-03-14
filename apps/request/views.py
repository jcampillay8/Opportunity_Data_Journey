from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import (View, TemplateView)
from django.contrib.auth.decorators import login_required
#from .forms.request_form_dash import RequestForm
from apps.request.forms.request_form_dash import app
from django.contrib.auth import logout
from apps.utils import get_context

# Create your views here.
def request_home(request):
    return render(request, 'request/request_home.html')


@login_required(login_url='login')
def new_request(request,pk):

    

    request.session['language'] = request.POST.get('language', 'English')
    #post = get_object_or_404(Post, id=pk)

    request.session['username'] = request.user.username

    context = {
     #   'post': post,
        'username': request.user.username
    }

    

    if pk == 8:
        return render(request, 'request/new_request.html', {'username': request.user.username, 'selected_language':get_context(request)})
    else:
        return render(request, 'request/formulario_no_disponible.html', context)

def request_history(request):
    return render(request, 'request/request_history.html',{'current_page': 'request_home','selected_language':get_context(request)})

def request_status(request):
    return render(request, 'request/request_status.html',{'current_page': 'request_home','selected_language':get_context(request)})
