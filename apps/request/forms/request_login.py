from django import forms
from django.forms import widgets
from ..models import Developer, Organization

#construimos un form usando las librerías de django ( que no depende de un objeto proveniente de models)
class LoginDeveloperForm(forms.Form): # LoginForm hereda de (forms.Form) porque es un formulario que no viene de un models!!!
    email = forms.EmailField(widget= forms.TextInput(attrs = {"class":"form-control ", "style":"width: 300px;"}), max_length=50, required=True)
    password = forms.CharField( widget= forms.PasswordInput(attrs = {"class":"form-control ", "style":"width: 300px;"}), required=True)



    def login(self, request):
        # comprueba sus validaciones (las que definí arriba)
        email = self.cleaned_data.get('email') 
        password = self.cleaned_data.get('password')

        user = Developer.authenticate(email, password)  
        return user 


class LoginOrganizationForm(forms.Form): # LoginForm hereda de (forms.Form) porque es un formulario que no viene de un models!!!
    email = forms.EmailField(widget= forms.TextInput(attrs = {"class":"form-control ", "style":"width: 300px;"}), max_length=50, required=True)
    password = forms.CharField( widget= forms.PasswordInput(attrs = {"class":"form-control ", "style":"width: 300px;"}), required=True)



    def login(self, request):
        # comprueba sus validaciones (las que definí arriba)
        email = self.cleaned_data.get('email') 
        password = self.cleaned_data.get('password')

        user = Organization.authenticate(email, password)  
        return user 

