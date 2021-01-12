from django import forms
from django.utils import timezone
from django.contrib.auth.forms import get_user_model

User=get_user_model()


from .models import OsobniInformace

class  RegisterForm(forms.ModelForm):


    class Meta:
        model   = OsobniInformace
        exclude=('user', 'gdpr', 'prispevky', 'lekarske_potvrzeni','image', 'je_zkontrolovan')