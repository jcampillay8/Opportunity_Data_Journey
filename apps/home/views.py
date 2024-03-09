import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from guest_user.decorators import allow_guest_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from functools import wraps
from django.contrib.auth.models import AnonymousUser
from django.views.generic import (View, TemplateView)
#from apps.contact.forms import ContactForm
from .forms import ContactForm
import traceback
from apps.utils import get_context
from core.settings import EMAIL_HOST_USER


class GuestUser:
    is_guest = True
    is_authenticated = False
    is_anonymous = False


def login_or_guest_required(func):
    @wraps(func)
    def decorated_view(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser) and not request.session.get('is_guest', False):
            return redirect('welcome')  # Redirigir a todos los usuarios anónimos que no son invitados a 'welcome'
        if request.user.is_authenticated:
            return login_required(login_url='/authentication/login')(func)(request, *args, **kwargs)
        elif request.session.get('is_guest', False):
            return allow_guest_user(func)(request, *args, **kwargs)
        else:
            return redirect('/authentication/login')
    return decorated_view


def guest_login(request):
    request.session['is_guest'] = True  # Establecer una variable de sesión para indicar que el usuario es un invitado
    return redirect('home')  # Redirigir al usuario a la página de inicio


@login_or_guest_required
def home(request):

    contact_form = ContactForm(request.POST or None)
    
    request.session['language'] = request.POST.get('language', 'English')
    print(type(get_context(request)))

    context = {
        'current_page': 'welcome',  # Cambia esto por el nombre de tu página
        'form':contact_form,
        'selected_language':get_context(request),
    }
    # Si el usuario no está autenticado o no es un invitado, redirigir a 'welcome'
    if not request.user.is_authenticated and not request.user.is_guest:

        return redirect('welcome',{ 'current_page': 'welcome','form':contact_form, 'selected_language':get_context(request) })
    # if request.method == 'POST':
    #     request.session['language'] = request.POST.get('language', 'English')

    return render(request, 'home/home.html',{ 'current_page': 'welcome','form':contact_form, 'selected_language':get_context(request) })


def welcome(request):
    if request.user.is_authenticated and not request.session.get('is_guest', False):
        return redirect('home')
    # Si se envía una solicitud POST, actualizar el idioma en la sesión
    if request.method == 'POST':
        request.session['language'] = request.POST.get('language', 'English')

    # Obtener los datos del idioma de la solicitud
    language_data = request.language_data
    
    # Determinar el idioma seleccionado por el usuario
    selected_language = request.session.get('language', 'English')
    
    # Obtener todos los datos del idioma seleccionado
    selected_language_data = language_data[selected_language]

    # Crear el contexto con los datos cargados
    context = {
        'selected_language': selected_language_data,
    }
    print(request)
    return render(request, 'partials/_welcome_content.html', context)


def contact_home(request):

    contact_form = ContactForm(request.POST or None)

    if request.method == "POST":

        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            content = request.POST.get('content', '')

            # Creamos el correo
            email = EmailMessage(
                "The Jaime Campillay Experience: Nuevo mensaje de contacto",
                "De {} <{}> <{}>\n\nEscribió:\n\n{}".format(name, email, phone, content),
                "no-contestar@inbox.mailtrap.io",
                ["opportunitydatajourney@gmail.com"],
                reply_to=[email]
            )  

            # Lo enviamos y redireccionamos
            try:
                email.send()
                return redirect(reverse('contact_home')+"?ok")
            except Exception as e:
                print(traceback.format_exc())
                return redirect(reverse('contact_home')+"?fail")

    return render(request, "home/home.html",{'form':contact_form,'current_page': 'welcome'})





