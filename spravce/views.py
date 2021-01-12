from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
import datetime

from .models import Skupina, Clenstvi, Kalendar
from ucty.models import OsobniInformace
from .forms import prehledForm, vytvorSkupinuForm, vyberSkupinuForm, checkForm, KalendarForm

from django.contrib.auth.models import Permission

User=get_user_model()
# Create your views here.
def my_try(value):
    try:
        v=int(value)
    except:
        v = 0
    return v

def prehled(request):
    form = prehledForm(request.POST or None)
    query= OsobniInformace.objects.all()
    ##################Vyhledavaci formular nahore#########################
    print('Pred:', request.POST)
    if form.is_valid():
        if request.POST.get('hledat'):
            print('TADY:',request.POST.get('hledat'))
            zadano = form.cleaned_data.get('vyhledavani')
            if zadano==[]:
                query = OsobniInformace.objects.all()
            else:
                if ',' in zadano:
                    zadano = zadano.rsplit(',')
                query = OsobniInformace.objects.none()
                print(zadano)
                for z in zadano:
                    print(type(z))
                    if '/' in z:
                        z=z.replace('/','')
                    print('zadano',my_try(z))
                    query|= OsobniInformace.objects.filter(user__username__icontains=z)or \
                            OsobniInformace.objects.filter(rodne_cislo__exact=z)or \
                            OsobniInformace.objects.filter(datum_narozeni__year__exact=my_try(z))
    ###########################Volby###################################
    if request.POST.get('zprava'):
        #request.session=request.POST.getlist('oznaceni')
        #return redirect(reverse_lazy('')) nová zprava
        ...
    if request.POST.get('skupiny'):
        request.session['ids']=request.POST.getlist('oznaceni')
        return redirect(reverse_lazy('pridat_do_skupiny'))
    if request.POST.get('prispevky'):
        zprava=''
        for id in request.POST.getlist('oznaceni'):
            user=OsobniInformace.objects.get(id=id)
            user.prispevky=True
            user.save()
            zprava+=f'{user.jmeno} {user.prijmeni}'
        if zprava != '':
            messages.success(request, f'Příspěvky byly nastaveny těmto členům: {zprava}')
        return redirect('prehled')
    return render(request, 'spravce/prehled.html',{ 'form':form,
                                                    'query':query,
                                                    })

def prava(request, id):
    mediator = Permission.objects.get(codename='Mediátor')
    spravce = Permission.objects.get(codename='Správce')
    user = OsobniInformace.objects.get(id=id)
    p = {'mediator': False, 'spravce': False}

    try:
        prava = user.user.user_permissions.all().get()
        if prava.name == 'Mediátor':
            p['mediator'] = True
        if prava.name == 'Správce':
            p['spravce'] =True
    except:
        pass

    if request.POST.get('mediator_odebrat'):
        user.user.user_permissions.remove(mediator)
        messages.success(request, f'{user.jmeno} {user.prijmeni} má odebrány práva MEDIÁTORA')
        return redirect('prehled')
    if request.POST.get('mediator_pridat'):
        user.user.user_permissions.add(mediator)
        messages.success(request,f'{user.jmeno} {user.prijmeni} má nastaveny práva MEDIÁTORA')
        return redirect('prehled')
    if request.POST.get('spravce_odebrat'):
        user.user.user_permissions.remove(spravce)
        messages.success(request,f'{user.jmeno} {user.prijmeni} má odebrány práva SPRÁVCE')
        return redirect('prehled')
    if request.POST.get('spravce_pridat'):
        user.user.user_permissions.add(spravce)
        messages.success(request,f'{user.jmeno} {user.prijmeni} má nastaveny práva SPRÁVCE')
        return redirect('prehled')

    return render(request, 'spravce/prava.html', {'prava':p, 'user':user})

def skupiny(request):
    form = vytvorSkupinuForm(request.POST or None)
    skupiny = Skupina.objects.all()
    if request.POST.get('vytvor_skupinu'):
        if form.is_valid():
            name=form.cleaned_data.get("nazev")
            form.save()
            messages.success(request, f'Skupina {name} byla vytvořena.')
            return redirect('skupiny')
    #zpravy
    if request.POST.get('napsat_trenerum'):
        ...
    if request.POST.get('napsat_vsem'):
        ...
    if id:=request.POST.get('vymazat_skupinu'):
        skupina = Skupina.objects.get(id=id)
        skupina.delete()
        messages.success(request,'Skupina byla vymazána')
        return redirect('skupiny')
    return render(request, 'spravce/skupiny.html', {'form':form, 'skupiny':skupiny})






def detailSkupiny(request, id):
    treneri=Clenstvi.objects.filter(skupina_id=id).filter(prava=True)
    clenove=Clenstvi.objects.filter(skupina_id=id).filter(prava=False)
    if uid:=request.POST.get('odstranit'):
        clenstvi = Clenstvi.objects.filter(user_id=uid).filter(skupina_id=id)
        clenstvi.delete()
        messages.success(request, 'Člen byl odstraněn ze skupiny')
        redirect('detail_skupiny', id)
    if uid:=request.POST.get('atlet'):
        clenstvi = Clenstvi.objects.filter(user_id=uid).filter(skupina_id=id).get()
        clenstvi.prava = False
        clenstvi.save()
        redirect('detail_skupiny', id)

    if uid:=request.POST.get('trener'):
        clenstvi = Clenstvi.objects.filter(user_id=uid).filter(skupina_id=id).get()
        clenstvi.prava = True
        clenstvi.save()
        redirect('detail_skupiny', id)
    return render(request,'spravce/detail_skupiny.html',{'treneri':treneri,
                                                         'clenove':clenove,
                                                         })

def pridatDoSkupiny(request):
    try:
        ids = request.session['ids']
    except:
        ids=[]
    form = vyberSkupinuForm(request.POST or None)
    print('IDS:',ids)
    if form.is_valid():
        if nazev:=form.cleaned_data.get('nazev'):
            Skupina.objects.create(nazev=nazev)
            return redirect('pridat_do_skupiny')
        if vyber:=form.cleaned_data.get('vyber'):
            print(vyber)
            skupina=Skupina.objects.get(nazev=vyber)
            zprava=''
            for id in ids:
                user=OsobniInformace.objects.get(id=id)
                Clenstvi.objects.create(user=user.user, skupina=skupina)
                zprava+=f' {user.jmeno} {user.prijmeni},'
            messages.success(request, f'Do skupiny {skupina} byli přidáni:{zprava}')
            try:
                del request.session['ids']
            except:
               pass
            return redirect('prehled')
    return render(request,'spravce/pridat_do_skupiny.html',{'form':form,})

def zkontrolovat(request, id):
    user=OsobniInformace.objects.get(id=id)
    form = checkForm(request.POST or None)
    if form.is_valid():
            user.je_zkontrolovan = True
            user.datum_vystaveni_lekarskeho_potvrzeni=form.cleaned_data.get('date')
            user.save()
            return redirect('prehled')
    return render(request,'spravce/check_user.html', {'form':form, 'user':user})

def kalendar(request):
    query = Kalendar.objects.filter(date__gt=datetime.datetime.now())
    form = KalendarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('kalendar')
    return render(request, 'spravce/kalendar.html', {'query':query, 'form':form})