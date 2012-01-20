# -*- coding: utf-8 -*-  
from django.shortcuts import render_to_response,redirect
from django.contrib import auth
from django.template import RequestContext
from NearsideBindings.base.forms import LoginForm,SignupForm,ImageCrop,ImageUpload
from NearsideBindings.base.utils import JsonResponse, upload_image
from NearsideBindings.settings import MEDIA_ROOT, MEDIA_URL, IMAGE_SAVE_CHOICES
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import Image, os

def index(request):
    if request.user.is_authenticated():
        return redirect('/members/%s/'% request.user.username)
    return render_to_response("index.html",locals(),context_instance=RequestContext(request))

def home(request):
    """timeline"""
    return render_to_response("home.html")

def signup(request):
    if request.method=="POST" and (not request.POST.has_key('from_mainpage')):
        form=SignupForm(request.POST)
        print form.errors
        if form.is_valid():
            new_user=form.save()
            login_user=auth.authenticate(username=new_user.username,password=request.POST['password1'])
            auth.login(request,login_user)
            return redirect('/members/%s/' % new_user.username)
    else:
        form=SignupForm()
        for name in ['last_name','email','student_num']:
            if request.POST.has_key(name):
                form.fields[name].widget.attrs['value']=request.POST[name]
    return render_to_response("accounts/signup.html",{'form':form},context_instance=RequestContext(request))


def login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user!=None:
                auth.login(request,user)
                if request.GET and request.GET.has_key('next'):
                    return redirect(request.GET['next'])
                return redirect('/members/%s/' % user.username)
            else:
                return render_to_response('accounts/login.html',context_instance=RequestContext(request))
    else: form=LoginForm()
    return render_to_response('accounts/login.html',{'form':form},context_instance=RequestContext(request))

@csrf_exempt
def upload(request):
    if request.method == "POST":
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            rlpath = upload_image(request.FILES['Filedata'])
            if rlpath:
                return JsonResponse({'path':rlpath})
            else:
                return HttpResponse('Uploading error')
        else:
            return HttpResponse('Invalid content')
    else:
        return HttpResponse('Bad request')

def crop(request,save_to):
    if request.method == "POST" and save_to in IMAGE_SAVE_CHOICES:
        form = ImageCrop(request.POST)
        if form.is_valid():
            now = datetime.now()
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            w = form.cleaned_data['w']
            h = form.cleaned_data['h']
            cw = form.cleaned_data['cw']
            ch = form.cleaned_data['ch']
            path = form.cleaned_data['path']
            filename = os.path.basename(path)
            abs_path = os.path.join(MEDIA_ROOT,'tmp',os.path.basename(path))
            img = Image.open(abs_path)
            rw = img.size[0]
            rh = img.size[1]
            x_rate = float(rw)/float(cw)
            y_rate = float(rh)/float(ch)
            x1 = int(round(x_rate*x))
            y1 = int(round(y_rate*y))
            x2 = int(round(x_rate*(x+w)))
            y2 = int(round(y_rate*(y+h)))
            box = (x1,y1,x2,y2)
            crop = img.crop(box)
            size = 150,150
            crop.thumbnail(size,Image.ANTIALIAS)
            base_path=os.path.join(MEDIA_ROOT,save_to)
            if not os.path.isdir(base_path):
                os.mkdir(base_path)
            date = now.strftime('%Y%m')
            date_path=os.path.join(base_path,date)
            if not os.path.isdir(date_path):
                os.mkdir(date_path)
            full_path = os.path.join(date_path,filename)
            crop.save(full_path)
            return JsonResponse({'path':os.path.join(MEDIA_URL,save_to,date,filename)})
        else:
            return HttpResponse('Bad Request')
    else:
        return HttpResponse('Permission Denied')