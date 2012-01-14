from django.shortcuts import render_to_response
from django.template import RequestContext
from NearsideBindings.activity.forms import HostActivity

def frontpage(requset):
    """docstring for group"""
    return render_to_response('activities/frontpage.html')

def single(request):
    return render_to_response('activities/single.html')

def host(request):
    form = HostActivity
    return render_to_response('activities/host.html', {'form':form,})