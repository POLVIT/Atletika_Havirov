from django import forms
from .models import Vykazy

class VykazForm(forms.ModelForm):
    vyber = forms.ChoiceField(choices=(('TR','trénink'),
                                       ('Z','závod'),
                                       ('S','soustředění'),
                                       ('J','jiná'),))
    class Meta:
        model=Vykazy
        exclude=('udalost','user',)