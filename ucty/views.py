from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
#K emailu
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode



def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            jmeno   =form.cleaned_data.get('jmeno')
            prijmeni=form.cleaned_data.get('prijmeni')
            email=form.cleaned_data.get('Email')
            #budouci username
            cele_jmeno=f'{jmeno} {prijmeni}'
            #V pripade duplicity jmen
            if User.objects.filter(username__exact=cele_jmeno):
                username=cele_jmeno+str(User.objects.filter(username__exact=cele_jmeno).count() + 1)
            else:
                username=cele_jmeno

            RC=form.cleaned_data.get('rodne_cislo')
            user=User.objects.create_user(username=username,password=RC)
            user.email=email
            user.is_active=False
            user.save()
            if not user:
                #Kdyz se to nepovede
                ...
            else:#Potvrzovaci email s prihlasovacimi udajy
                current_site = get_current_site(request)
                subject = 'Potvrzení přihlášky do Atletiky Havířov 1965'
                message = render_to_string('ucty/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'username':username,
                    'RC':RC,
                })
                user.email_user(subject, message)
                messages.success(request, ('Prosím potvrďte svou přihlášku na emailu.'))
                prihlaska=form.save(commit=False)
                prihlaska.user=user
                prihlaska.save()
                return redirect('/')

    else:
        form=RegisterForm()
    return render(request,'ucty/register.html', {'form':form})

def activate(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, ('Potvrzení proběhlo v pořádku'))
        return redirect('home')
    else:
        messages.warning(request, ('Potvrzení se nezdařilo'))
        return redirect('home')

@login_required
def home(request):
    return render(request, 'ucty/home_po_prihlaseni.html',{})