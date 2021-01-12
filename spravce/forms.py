from django import forms
from .fileds import CommaSeparatedCharField
from .models import Skupina, Kalendar

class prehledForm(forms.Form):
    vyhledavani = CommaSeparatedCharField(required=False)



class vytvorSkupinuForm(forms.ModelForm):
    class Meta:
        model=Skupina
        fields=['nazev',]

class vyberSkupinuForm(forms.Form):
    nazev=forms.CharField(max_length=255, required=False)
    vyber=forms.ModelChoiceField(queryset=Skupina.objects.all(), empty_label='-------------------------', required=False)

class checkForm(forms.Form):
    date = forms.DateField(required=True)

class KalendarForm(forms.ModelForm):
    class Meta:
        model=Kalendar
        fields='__all__'