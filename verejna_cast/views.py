from django.shortcuts import render

# Create your views here.

def uvodniStranka(request):
    return render(request,'verejna_cast/uvod.html',{})