from django import forms
from django.contrib.admin import widgets
from .fileds import CommaSeparatedCharField
from django.contrib.auth.forms import get_user_model
from .models import PrispevekProMediatora, PrispevekFiles, createPost
User=get_user_model()




from django.forms import ClearableFileInput



class PPMText(forms.ModelForm):  #Prispevek Pro Mediatora.....
    class Meta:
        model = PrispevekProMediatora
        fields = ['text']

class PPMFiles(forms.ModelForm):
    class Meta:
        model = PrispevekFiles
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class FotoForm(forms.ModelForm):
    oznaceni = forms.BooleanField(required=False)
    class Meta:
        model=PrispevekFiles
        fields=['file',]
        widgets = {}

class CreatePostForm(forms.ModelForm):
    url=CommaSeparatedCharField(required=False, widget=forms.widgets.Textarea())
    class Meta:
        model = createPost
        exclude = ('fb_post', 'ig_post', 'web_post_succes')
        widgets={'foto_urls':forms.HiddenInput,

                 }




class uploadFileForm(forms.Form):
    file=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) #attrs={'multiple': True}
