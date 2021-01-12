from django.shortcuts import render, redirect ,HttpResponseRedirect, reverse
from django.contrib.auth.decorators import permission_required, login_required
from .models import PrispevekProMediatora, PrispevekFiles, createPost
from .forms import PPMText,PPMFiles, CreatePostForm, uploadFileForm
from django.contrib import messages
from django.core.files.storage import default_storage
import os
from django.core.files.base import ContentFile
from Atletika_Havirov.settings import MEDIA_URL

def url_v_uloziste():
    basepath = '/home/vit/Atletika_Havirov/media/prispevky/ulozene'
    basepath = '/home/vit/Atletika_Havirov/media/prispevky/ulozene'
    urls = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            urls.append(os.path.join(MEDIA_URL + 'prispevky/ulozene', entry))
    return urls



# Create your views here.
@login_required
@permission_required('ucty.mediator')
def mediatorHome(request):
    prispevky=PrispevekProMediatora.objects.all()

    return render(request,'mediator/mediator_home.html',{'prispevky':prispevky})

@login_required
@permission_required('ucty.mediator')
def detailPrispevku(request, id):
    prispevek = PrispevekProMediatora.objects.get(id=id)
    fotky = prispevek.prispevekfiles_set.all()


    if request.POST.get('ulozit'):
        for fotka in fotky:
            if request.POST.get(f'{fotka.id}'):
                    path = f'/home/vit/Atletika_Havirov{fotka.file.url}'
                    new_file = default_storage.open(path).read()
                    default_storage.save(f'/home/vit/Atletika_Havirov/media/prispevky'
                                         f'/ulozene/{fotka.file.url.rsplit("/", 1)[-1]}',
                                         ContentFile(new_file))

    if request.POST.get('smazat'):
        for fotka in fotky:
            if request.POST.get(f'{fotka.id}'):
                path='/home/vit/Atletika_Havirov'+fotka.file.url
                if os.path.isfile('/home/vit/Atletika_Havirov/'+fotka.file.url):
                    os.remove(path)
                fotka.delete()
        return redirect('detail_prispevku', id=id)

    if request.POST.get('PouzitCele'):
        paths=''
        for file in prispevek.prispevekfiles_set.all():
                paths+=f'{file.file.url},'


        request.session['text'] = prispevek.text
        request.session['paths']= paths
        return redirect('mediator_novy_prispevek')





    return render(request, 'mediator/mediator_prispevek_detail.html', {'prispevek': prispevek,
                                                                       'fotky': fotky,
                                                                       })



@login_required
@permission_required('ucty.mediator')
def nahrajData(request):
    if request.method == 'POST':
        form = PPMText(request.POST)
        file_form = PPMFiles(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            prispevek = form.save()
            for f in files:
                file_instance = PrispevekFiles(file=f, prispevek=prispevek)
                file_instance.save()
            messages.success(request, 'Příspěvek byl nahrán, děkujeme!')
            return redirect('mediator_home')
    else:
        form = PPMText()
        file_form = PPMFiles()
    return render(request,'mediator/upload.html', {'form':form, 'files':file_form})

@login_required
@permission_required('ucty.mediator')
def _novyPrispevek(request):
    print('___________NOVY_____________')
    #dostanu vsechny url fotek v ulozisti
    urls = url_v_uloziste()
    #musim osetrit vymazani session
    try:
        url_uloziste = request.session.get('paths')
        print('NAHORE:', url_uloziste)
        del request.session['paths']
    except KeyError:
        url_uloziste=''

    try:
        text = request.session['text']
        del request.session['text']
    except KeyError:
        text=''
    print('NAHORE request pred POST:', request.POST.get('nahratModal'))
    #Modal tzn. nahravani fotek z uloziste
    if request.method=='POST':
        print('NAHORE v POST:', url_uloziste)
        post = CreatePostForm(request.POST)
        post.initial = {'url': url_uloziste, 'text': text}
        if request.POST.get('nahratModal'):
            for url in urls:
                if request.POST.get(f'{url}'):
                    if url_uloziste == '':
                        url_uloziste+=f'{url}'
                    else:
                        url_uloziste += f',\n{url}'
            print(url_uloziste)
            request.session['text']=text
            request.session['paths']=url_uloziste
            return redirect('mediator_novy_prispevek')

        elif request.POST.get('delete'):
            print('Request:',request.POST.get('delete'))
            print('Uloziste:',url_uloziste)


        if post.is_valid() and request.POST.get('nahrat'):
            post.save(commit=False)
            createPost.objects.create(fb_time=post.cleaned_data.get('fb_time'),
                                      ig_time=post.cleaned_data.get('ig_time'),
                                      web_post=post.cleaned_data.get('web_post'),
                                      titulek=post.cleaned_data.get('titulek'),
                                      text=post.cleaned_data.get('text'),
                                      foto_urls=post.cleaned_data.get('url'))
            messages.success(request,'Váš příspěvek byl vytvořen')
            return redirect('pripravene')
    else:
        post = CreatePostForm()
        post.initial = {'url':url_uloziste, 'text': text}
        #request.session['paths']:url_uloziste
        #request.session['text']:text

    return render(request, 'mediator/pripravit_prispevek.html', context= {'form':post,
                                                                          'urls':urls, #urls v ulozisti (MODAL)
                                                                          'URL':url_uloziste.rsplit(',') if url_uloziste.__len__() > 0 else None
                                                                          }) #url zadané do pole URL


@login_required
@permission_required('ucty.mediator')
def novyPrispevek(request, id=None):
    url_uloziste = url_v_uloziste() #data pro modal
    try:
        urls = request.session.get('paths')
        if not urls: urls = '' #je to tu k vuli podmince v poslednim returnu, urls nesmi byt None
    except KeyError: urls = ''

    try: text = request.session.get('text')
    except KeyError: text = ''


    if request.method=='POST':
        post = CreatePostForm(request.POST)
        if id:
            p=createPost.objects.get(id=id)
            post.initial = {'text': text, 'url': urls, 'fb_time': p.fb_time, 'ig_time':p.ig_time,
                            'web_post':p.web_post, 'titulek':p.titulek}
        else:
            post.initial = {'text': text, 'url': urls}
        ######################################################
        if request.POST.get('nahratModal'):
            for url in url_uloziste:
                if request.POST.get(f'{url}'): urls+=f'{url},'
            request.session['paths']=urls
            if id:
                return redirect('mediator_novy_prispevek', id)
            else:
                return redirect('mediator_novy_prispevek')
        ###################################################
        if request.POST.get('delete'):
            urls=urls.replace(f"{request.POST.get('delete')},",'')
            request.session['paths']=urls
            if id:
                return redirect('mediator_novy_prispevek', id)
            else:
                return redirect('mediator_novy_prispevek')
        ###################################################
        if request.POST.get('reorder'):
            urls=urls.replace(f"{request.POST.get('reorder')},",'')
            urls=f"{request.POST.get('reorder')},"+urls
            request.session['paths']=urls
            if id:
                return redirect('mediator_novy_prispevek', id)
            else:
                return redirect('mediator_novy_prispevek')
        ######################################################
        if request.POST.get('nahrat') and post.is_valid():
            post.save(commit=False)
            if id:
                prispevek = createPost.objects.get(id=id)
                prispevek.fb_time=post.cleaned_data.get('fb_time')
                prispevek.ig_time=post.cleaned_data.get('ig_time')
                prispevek.web_post=post.cleaned_data.get('web_post')
                prispevek.titulek=post.cleaned_data.get('titulek')
                prispevek.text=post.cleaned_data.get('text')
                prispevek.foto_urls=post.cleaned_data.get('url')
                prispevek.save()
                messages.success(request, 'Váš příspěvek byl aktualizován')
            else:
                createPost.objects.create(fb_time=post.cleaned_data.get('fb_time'),
                                          ig_time=post.cleaned_data.get('ig_time'),
                                          web_post=post.cleaned_data.get('web_post'),
                                          titulek=post.cleaned_data.get('titulek'),
                                          text=post.cleaned_data.get('text'),
                                          foto_urls=post.cleaned_data.get('url'))
                messages.success(request, 'Váš příspěvek byl vytvořen')
            try:    del request.session['paths']
            except KeyError: pass
            try:    del request.session['text']
            except KeyError: pass
        return redirect('pripravene')
        ######################################################
    else:
        post=CreatePostForm()
        if id:
            p = createPost.objects.get(id=id)
            post.initial = {'text': text, 'url': urls, 'fb_time': p.fb_time, 'ig_time': p.ig_time,
                            'web_post': p.web_post, 'titulek': p.titulek}
        else:
            post.initial = {'text': text, 'url': urls}
    return render(request, 'mediator/pripravit_prispevek.html',
                  context={'form': post,
                           'urls': url_uloziste,  # urls v ulozisti (MODAL)
                           'URL': urls[0:-1].rsplit(',') if urls.__len__() > 0 else None # url zadané do pole URL
                           })





@login_required
@permission_required('ucty.mediator')
def uloziste(request):
    urls = url_v_uloziste()
    if request.method=='POST':
        form = uploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file'):
                new_file=f.read()
                default_storage.save(f'/home/vit/Atletika_Havirov/media/prispevky'
                                     f'/ulozene/{f}',ContentFile(new_file))
            return redirect('uloziste')
    else:
        form = uploadFileForm()
    return render(request, 'mediator/uloziste.html', {'urls':urls,'form':form,})


def pripravene(request):
    prispevky=createPost.objects.all().order_by('-id')

    return render(request, 'mediator/pripravene.html', {'prispevky':prispevky})

def updatePrispevku(request, id):
    prispevek = createPost.objects.get(id=id)
    p=prispevek.foto_urls
    forbiden = ["[","]","'",'"']
    for f in forbiden:p=p.replace(f,'')
    request.session['text'] = prispevek.text
    request.session['paths'] = p+','
    return redirect('mediator_novy_prispevek', id)



def kopiePrispevku(request, id):
    prispevek = createPost.objects.get(id=id)
    p = prispevek.foto_urls
    forbiden = ["[", "]", "'", '"']
    for f in forbiden: p = p.replace(f, '')
    request.session['text'] = prispevek.text
    request.session['paths'] = p + ','
    return redirect('mediator_novy_prispevek')

