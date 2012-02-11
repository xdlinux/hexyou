# -*- coding: utf-8 -*-  
from django.db.models import Count
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from NearsideBindings.activity.forms import ActivityForm
from NearsideBindings.activity.models import *
from NearsideBindings.group.models import Group, MemberShip
from NearsideBindings.activity.signals import inform
# from django.core.exceptions import DoesNotExist

@login_required
def frontpage(request):
    """docstring for group"""
    types = ActivityType.objects.all()
    location_roots = Location.objects.filter(parent=0)
    top_activity = Activity.objects.order_by('?')
    activities = Activity.objects.order_by('-id')[:8].annotate(Count('participators'))
    hot_activities = Activity.objects.annotate(Count('participators')).order_by('-participators__count')[:4]
    for activity in activities:
        activity.host_string = activity.get_host_string()
    if top_activity:
        top_activity=top_activity[0]
        host_string = top_activity.get_host_string()
    return render_to_response('activities/frontpage.html',locals(), context_instance=RequestContext(request))

@login_required
def single(request,activity_id):
    activity = get_object_or_404(Activity,id=int(activity_id))
    host_string = activity.get_host_string()
    return render_to_response('activities/single.html',locals(), context_instance=RequestContext(request))

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
            subject = u"[活动]"+ activity.title + u" " + activity.get_host_string(False)
            body = ''
            for member in form.cleaned_data['inform_users']:
                inform(subject,body,User.objects.get(pk=member))
            return redirect("/activities/%s" % activity.id)
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,'location_roots':location_roots}, context_instance=RequestContext(request))
