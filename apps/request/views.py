from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import (View, TemplateView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from .forms.request_form_dash import RequestForm
from apps.request.models import CotizacionRealizada, CotizacionRealizada_Productos, CotizacionRealizada_Archivos, Estado_Solicitudes
from apps.request.forms.request_form_dash import app
from apps.request.forms.request_status_form import app
from apps.request.forms.revision_solicitud import app

from django.contrib.auth import logout
from apps.utils import get_context


# Create your views here.
@login_required(login_url='login')
def request_home(request):
    return render(request, 'request/request_home.html',{'current_page': 'request_home'})


@login_required(login_url='login')
def new_request(request,pk):

    user = User.objects.get(username=request.user.username)

    request.session['language'] = request.POST.get('language', 'English')
    #post = get_object_or_404(Post, id=pk)

    screen_width = request.COOKIES.get('screen_width')

    context = {
     #   'post': post,
        'user_id' : user.id,
        'username': user.username,
        'screen_width': screen_width,
        'current_page': 'request_home',
    }
    

    if pk == 8:
        return render(request, 'request/new_request.html', context)
        #return render(request, 'request/new_request.html', {'user_id' : user.id, 'username': request.user.username, 'selected_language':get_context(request)})
    else:
        return render(request, 'request/formulario_no_disponible.html', context)

def request_history(request):
    return render(request, 'request/request_history.html',{'current_page': 'request_home','selected_language':get_context(request)})

# @login_required(login_url='login')
# def request_status(request):
#     return render(request, 'request/request_status.html',{'current_page': 'request_home','selected_language':get_context(request)})


def request_status(request):
    screen_width = request.COOKIES.get('screen_width')
    context = {
        'current_page': 'request_home',
        'selected_language': get_context(request),
        'screen_width': screen_width,
    }
    return render(request, 'request/request_status.html', context)


# @login_required(login_url='login')
# def revision_solicitud(request, id):
#     request.session['id'] = id  
#     return render(request, 'request/revision_solicitud.html')


@login_required(login_url='login')
def revision_solicitud(request, id):
    request.session['id'] = id
    screen_width = request.COOKIES.get('screen_width')
    context = {
        'current_page': 'request_home',
        'selected_language': get_context(request),
        'screen_width': screen_width,
    }
    return render(request, 'request/revision_solicitud.html', context)
