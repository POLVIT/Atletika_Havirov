from django.urls import path
from .views import prava,prehled, skupiny, detailSkupiny, pridatDoSkupiny,zkontrolovat, kalendar

urlpatterns = [
    path('prava/<id>/',prava, name='prava'),
    path('prehled/', prehled, name='prehled'),
    path('skupiny/', skupiny, name='skupiny'),
    path('skupiny/<id>/',detailSkupiny, name='detail_skupiny' ),
    path('pridat-cleny/',pridatDoSkupiny, name='pridat_do_skupiny'),
    path('zkontrolovat/<id>', zkontrolovat, name='zkontrolovat'),
    path('kalendar/', kalendar, name='kalendar')
]