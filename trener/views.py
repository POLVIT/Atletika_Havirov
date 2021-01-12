from django.shortcuts import render
from .forms import VykazForm
from .models import Vykazy

import datetime
# Create your views here.

def vykaz(request, uid): #user ID
    form = VykazForm()
    vykazy = Vykazy.objects.filter(user_id=uid)
    return render(request,'trener/vykaz.html',{'form':form,
                                               'vykazy':vykazy,
                                               })