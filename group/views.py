from django.shortcuts import render_to_response
from NearsideBindings.group.forms import FoundGroup


def frontpage(requset):
    """docstring for group"""
    return render_to_response('groups/frontpage.html')

def single(request):
    return render_to_response('groups/single.html')

def found(request):
    form = FoundGroup
    return render_to_response('groups/found.html', {'form':form,})