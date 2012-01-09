# Create your views here.
from django.shortcuts import render_to_response,redirect
from django.contrib import auth


def frontpage(request):
    """docstring for person"""
    return render_to_response('members/frontpage.html')

def single(request,username):
    """docstring for person"""
    if request.user.is_authenticated() and request.user.username==username:
        return render_to_response('members/single.html',{'user':request.user})
    else: return redirect('/')
