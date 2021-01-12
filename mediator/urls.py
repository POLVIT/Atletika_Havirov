from django.urls import path, include



from .views import (mediatorHome, detailPrispevku, nahrajData, novyPrispevek, uloziste, pripravene,
                    kopiePrispevku,updatePrispevku,)


urlpatterns = [
    path('',mediatorHome, name='mediator_home'),
    path('detail/<id>/', detailPrispevku, name='detail_prispevku'),
    path('upload/',nahrajData, name='vytvor_prispevek'),
    path('new/', novyPrispevek, name='mediator_novy_prispevek'),
    path('new/<id>/', novyPrispevek, name='mediator_novy_prispevek'),
    path('new/kopie/<id>/', kopiePrispevku, name='kopie_prispevku'),
    path('new/update/<id>/',updatePrispevku, name='update_prispevku'),
    path('uloziste/', uloziste, name='uloziste'),
    path('pripravene/', pripravene, name='pripravene'),




]