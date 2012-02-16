# -*- coding: utf-8 -*-  
from django.core.paginator import InvalidPage, EmptyPage
from django.db.models import Count
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden
from NearsideBindings.activity.forms import ActivityForm, EditActivityForm
from NearsideBindings.activity.models import *
from NearsideBindings.group.models import Group, MemberShip
from NearsideBindings.base.utils import ExPaginator, inform
from django.template.loader import get_template
from django.template import Context
# from django.core.exceptions import DoesNotExist

@login_required
def frontpage(request):
    """docstring for group"""
    types = ActivityType.objects.all().values()
    location_roots = Location.objects.filter(parent=None)
    top_activity = Activity.objects.order_by('?')
    activities = Activity.objects.select_related().order_by('-id')[:8].annotate(Count('members'))
    hot_activities = Activity.objects.annotate(members_count=Count('members')).order_by('-members_count')[:4]
    if top_activity:
        top_activity=top_activity[0]
    return render_to_response('activities/frontpage.html',locals(), context_instance=RequestContext(request))

@login_required
def single(request,activity_id):
    activity = get_object_or_404(Activity,id=int(activity_id))
    activity_members = activity.members.all()[:8]
    activity_members_count = activity.members.count()
    related_activities = Activity.objects.filter(location=activity.location).order_by('?')[:4].annotate(Count('members'))
    photos = activity.photos.all().values()
    try:
        membership = MemberHostShip.objects.get(activity=activity,user=request.user)
        is_host,is_participator=membership.is_host, True
    except MemberHostShip.DoesNotExist:
        is_host,is_participator = False,False
    return render_to_response('activities/single.html',locals(), context_instance=RequestContext(request))

@login_required(login_url="/login/")
def create(request):
    location_roots = Location.objects.filter(parent=None)
    if request.POST:
        form=ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            memberhost = MemberHostShip(is_host=True,activity=activity,user=request.user)
            memberhost.save()
            for host_group in form.cleaned_data['host_groups']:
                group = Group.objects.get(pk=host_group)
                hostship = HostShip(activity=activity,group=group)
                if MemberShip.objects.get(group=group,user=request.user).is_admin:
                    hostship.accepted = True
                hostship.save()
            subject = u"[活动]"+ activity.title + u" " + activity.get_host_string(False)
            t = get_template('activities/create_inform.html')
            body = t.render(Context({'activity':activity}))
            for member in form.cleaned_data['inform_users']:
                inform(subject,body,User.objects.get(pk=member))
            return redirect("/activities/%s" % activity.id)
    else:
        form=ActivityForm()
    return render_to_response('activities/host.html', {'form':form,'location_roots':location_roots}, context_instance=RequestContext(request))

@login_required
def random(request):
    activity = Activity.objects.order_by('?')[0]
    return redirect('/activities/%s' % str(activity.pk) )

@login_required
def my(request,is_host):
    is_host = is_host == 'hosted'
    paginator = ExPaginator(Activity.objects.filter(members=request.user,memberhostship__is_host=is_host).annotate(Count('members')),8)
    try:
        page = int(request.GET.get('page'))
    except (ValueError, TypeError):
        page = 1
    try:
        activities = paginator.page(page)
    except (EmptyPage, InvalidPage):
        activities = paginator.page(paginator.num_pages)
    return render_to_response('activities/my.html',locals(),context_instance=RequestContext(request))

@login_required
def sort(request,by,token):
    hot_activities = Activity.objects.annotate(members_count=Count('members')).order_by('-members_count')[:4]
    if by == "type":
        activities = Activity.objects.filter(activity_type__id=token).annotate(Count('members'))
        activity_type = ActivityType.objects.get(id=token)
    elif by == "location":
        activities = Activity.objects.filter(location__id=token).annotate(Count('members'))
        location = Location.objects.get(id=token)
    else:
        return HttpResponseNotFound()
    paginator = ExPaginator(activities,8)
    try:
        page = int(request.GET.get('page'))
    except (ValueError, TypeError):
        page = 1
    try:
        activities = paginator.page(page)
    except (EmptyPage, InvalidPage):
        activities = paginator.page(paginator.num_pages)
    return render_to_response('activities/sort.html',locals(),context_instance=RequestContext(request))

@login_required
def edit(request,activity_id):
    activity = get_object_or_404(Activity,id=int(activity_id))
    location_roots = Location.objects.filter(parent=None).values()
    group_accepted = activity.host_groups.filter(hostship__accepted=True).count()
    if request.POST:
        form = EditActivityForm(request.POST)
    else:
        form = EditActivityForm()
    return render_to_response('activities/edit.html',locals(),context_instance=RequestContext(request))

@login_required
def cancel(request,activity_id):
    activity = get_object_or_404(Activity,id=int(activity_id))
    group_accepted = activity.host_groups.filter(hostship__accepted=True).count()
    is_host = MemberHostShip.objects.get(user=request.user,activity=activity).is_host
    if group_accepted or not is_host :
        return HttpResponseForbidden()
    activity.members.clear()
    activity.host_groups.clear()
    activity.delete()
    return redirect('activities')
