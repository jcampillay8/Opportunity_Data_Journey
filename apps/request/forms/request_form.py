from django import forms
from apps.request.models import Request

class RequestForm(forms.ModelForm):
    CHOICES=[('select1','select 1'),
             ('select2','select 2')]

    radios = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Request
        fields = ['text', 'number', 'date', 'dropdown', 'checkbox1', 'checkbox2', 'checkbox3', 'radios', 'range', 'file', 'textarea']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }