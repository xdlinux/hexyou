# -*- coding: utf-8 -*-  
from django.shortcuts import render_to_response,redirect
from django.contrib import auth
from django.template import RequestContext
from NearsideBindings.base.forms import LoginForm,SignupForm

def index(request):
    """index"""
    return render_to_response("index.html",locals(),context_instance=RequestContext(request))

def home(request):
    """timeline"""
    return render_to_response("home.html")

def signup(request):
    if request.method=="POST" and (not request.POST.has_key('from_mainpage')):
        form=SignupForm(request.POST)
        if form.is_valid():
            print "do something to create an user"
            return ""
    else:
        form=SignupForm()
        for name in ['fullname','email','student_num']:
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
                return redirect('/%s/' % user.id)
            else:
                return render_to_response('accounts/login.html',{'error','认证失败，请确认您的用户名和密码输入正确'},context_instance=RequestContext(request))
    else: form=LoginForm()
    return render_to_response('accounts/login.html',{'form':form},context_instance=RequestContext(request))
    

