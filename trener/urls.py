from django.urls import path, include
from .views import vykaz

urlpatterns = [
    path('vykaz/<uid>/', vykaz, name='vykaz'),

]