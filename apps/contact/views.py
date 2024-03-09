from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.views.generic import (View, TemplateView)
from apps.utils import get_context
import traceback


def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            content = request.POST.get('content', '')
            print(phone)

            # Creamos el correo
            email = EmailMessage(
                "The Jaime Campillay Experience: Nuevo mensaje de contacto",
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, phone, content),
                "no-contestar@inbox.mailtrap.io",
                ["thejaimecampillayexperience@gmail.com"],
                reply_to=[email]
            )

            try:
                email.send()
                return redirect(reverse('contact')+"?ok")
            except Exception as e:
                print(traceback.format_exc())
                return redirect(reverse('contact')+"?fail")
    
    return render(request, "contact/contact.html",{'form':contact_form,'current_page': 'contact','selected_language':get_context(request)})