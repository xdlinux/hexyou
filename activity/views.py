from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from NearsideBindings.activity.forms import ActivityForm
from NearsideBindings.activity.models import *
from NearsideBindings.group.models import Group, MemberShip
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
# from django.core.exceptions import DoesNotExist


def frontpage(request):
    """docstring for group"""
    types = ActivityType.objects.all()
    location_roots = Location.objects.filter(parent=0)
    top_activity = Activity.objects.order_by('?')[0]
    top_activity_groups = top_activity.host_group.all()
    return render_to_response('activities/frontpage.html',locals())

def single(request,activity_id):
    activity = get_object_or_404(Activity,id=int(activity_id))
    groups = activity.host_groups.all()
    hosts = activity.hosts.all()
    fullhostship = []
    for host in hosts:
        try:
            real_groups = Group.objects.filter(members=host)
        except 'DoesNotExist':
            pass
        else:
            fullhostship.append({'host':host,'groups':set(groups) & set(real_groups)})
    return render_to_response('activities/single.html',locals())

@login_required(login_url="/login/")
def create(request):
    location_roots = Location.objects.filter(parent=0)
    if request.POST:
        form=ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            activity.hosts.add(request.user)
            for host_group in form.cleaned_data['host_groups']:
                group = Group.objects.get(pk=host_group)
                hostship = HostShip(activity=activity,group=group)
                hostship.save()
            return redirect("/activities/%s" % activity.id)
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,'location_roots':location_roots}, context_instance=RequestContext(request))
