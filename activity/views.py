from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from NearsideBindings.activity.forms import ActivityForm
from NearsideBindings.activity.models import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse


def frontpage(request):
    """docstring for group"""
    types = ActivityType.objects.all()
    location_roots = Location.objects.filter(parent=0)
    top_activity = Activity.objects.order_by['?'][0]
    return render_to_response('activities/frontpage.html',locals())

def single(request,activity_id):
    activity = get_object_or_404(id=int(activity_id))
    return render_to_response('activities/single.html',locals())

@login_required(login_url="/login/")
def create(request):
    location_roots = Location.objects.filter(parent=0)
    if request.POST:
        form=ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            activity.hosts = [request.user,]
            form.save_m2m()
            redirect("activities/%s",activity.id)
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,'location_roots':location_roots}, context_instance=RequestContext(request))
