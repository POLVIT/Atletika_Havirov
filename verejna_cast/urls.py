from django.urls import path
from .views import uvodniStranka

urlpatterns = [
    path('', uvodniStranka,name='uvod'),

]