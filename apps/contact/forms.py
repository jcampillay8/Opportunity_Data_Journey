from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    name = forms.CharField(label="Nombre", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escribe tu nombre'}
    ), min_length=3, max_length=100)
    last_name = forms.CharField(label="Apellido", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escribe tu Apellido'}
    ), min_length=3, max_length=100)
    # email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
    #     attrs={'class':'form-control', 'placeholder':'Escribe tu email'}
    # ), min_length=3, max_length=100)
    phone = forms.CharField(validators=[phone_regex], label="Phone", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escribe tu telefono'}
    ), min_length=3, max_length=100)
    content = forms.CharField(label="Contenido", required=True, widget=forms.Textarea(
        attrs={'class':'form-control', 'rows': 3, 'placeholder':'Escribe tu mensaje'}
    ), min_length=10, max_length=1000)
