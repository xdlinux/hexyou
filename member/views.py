# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect
from django.contrib import auth


def frontpage(request):
    """docstring for person"""
    return render_to_response('members/frontpage.html')

def single(request,username):
    """docstring for person"""
    if request.user.is_authenticated(): 
        return render_to_response('members/single.html',{'user':request.user,'is_me':request.user.username==username})
    else: return redirect('/')

@login_required(login_url='/login/')
def profile(request):
    return single(request,request.user.username)
