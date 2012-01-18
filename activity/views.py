from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from NearsideBindings.activity.forms import ActivityForm
from django.contrib.auth.decorators import login_required

def frontpage(request):
    """docstring for group"""
    return render_to_response('activities/frontpage.html')

def single(request):
    return render_to_response('activities/single.html')

@login_required(login_url="/login/")
def create(request):
    if request.POST:
        form=ActivityForm(request.POST)
        if form.is_valid():
            #do something
            pass
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,})
