from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from NearsideBindings.activity.forms import ActivityForm
from NearsideBindings.activity.models import Location
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse


def frontpage(request):
    """docstring for group"""
    return render_to_response('activities/frontpage.html')

def single(request):
    return render_to_response('activities/single.html')

@login_required(login_url="/login/")
def create(request):
    location_roots = Location.objects.filter(parent=0)
    if request.POST:
        form=ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.hosts = [request.user,]
            activity.save()
            redirect("activities/%s",activity.slug)
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,'location_roots':location_roots}, context_instance=RequestContext(request))
