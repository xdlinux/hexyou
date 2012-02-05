# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from NearsideBindings.group.models import MemberShip
from NearsideBindings.member.forms import EditProfileForm
from django import forms
from NearsideBindings.base.utils import get_gravatar_url
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm


def frontpage(request):
    """docstring for person"""
    return render_to_response('members/frontpage.html')

@login_required(login_url='/login/')
def single(request,username):
    """docstring for person"""
    user = User.objects.get(username=username)
    groups = [ membership.group for membership in MemberShip.objects.filter(user=user) ]
    return render_to_response('members/single.html',{'user':user,'groups':groups,'group_counter':len(groups),'is_me':request.user.username==username})

@login_required(login_url='/login/')
def profile(request):
    return single(request,request.user.username)
    # return render_to_response('members/single.html',{'user':request.user,'is_me':True})

@login_required(login_url='/login/')
def edit_profile(request):
    request.user.avatar = request.user.avatar or get_gravatar_url(request.user.email)
    if request.POST:
        form = EditProfileForm(request.POST,instance=request.user)
        if form.is_valid(): form.save()
        if request.POST.has_key('old_password'):
            passform=PasswordChangeForm(request.user,request.POST)
            if passform.is_valid() : passform.save()
        else:
            passform=PasswordChangeForm(request.user)
    else:
        form = EditProfileForm(instance=request.user)
        passform=PasswordChangeForm(request.user)
    return render_to_response('members/edit.html',{'user':request.user,'form':form,'is_me':True,'passform':passform},context_instance=RequestContext(request))
