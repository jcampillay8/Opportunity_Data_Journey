from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import ContactForm
from django.views.generic import (View, TemplateView)
from django.views.decorators.csrf import csrf_exempt
from apps.utils import get_context
import traceback

@csrf_exempt
def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            last_name = request.POST.get('last_name', '')
            email = request.user.email  # Corrección aquí
            phone = request.POST.get('phone', '')
            content = request.POST.get('content', '')
            print(phone)

            # Creamos el correo
            email = EmailMessage(
                "The Jaime Campillay Experience: Nuevo mensaje de contacto",
                "De {} {}<Email: {}><Phone: {}>\n\nEscribió:\n\n{}".format(name, last_name, email, phone, content),
                "no-contestar@inbox.mailtrap.io",
                ["opportunitydatajourney@gmail.com"],
                reply_to=[email]
            )

            try:
                email.send()
                messages.success(request, 'Su mensaje se ha enviado correctamente, en breve nos pondremos en contacto con usted.')
                return redirect(reverse('contact')+"?ok")
            except Exception as e:
                print(traceback.format_exc())
                return redirect(reverse('contact')+"?fail")

    # Obtén el usuario logueado
    user = request.user

    # Pasa el usuario como contexto a la plantilla
    return render(request, "contact/contact.html",{'form':contact_form, 'user': user, 'current_page': 'contact','selected_language':get_context(request)})
