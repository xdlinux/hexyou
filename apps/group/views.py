# -*- coding: utf-8 -*-  
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.template import Context,RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response,redirect,get_object_or_404
from activity.models import Activity, HostShip
from base.utils import ExPaginator, inform
from group.forms import NewGroupForm, AdminGroupForm
from group.models import Group,MemberShip

def get_top_group():
    top_group = Group.objects.exclude(description="").exclude(avatar="/static/images/no_avatar.png").order_by('?').values()
    if top_group:
        top_group=top_group[0]
        top_group_members = MemberShip.objects.filter(group__id=top_group['id']).count()
        return top_group, top_group_members, True
    else: return None,None,False

@login_required(login_url='/login/')
def frontpage(request):
    """docstring for group"""
    managed_groups = [ membership.group for membership in MemberShip.objects.filter(user=request.user,is_admin=True) ]
    managed_counter = len(managed_groups)
    joined_groups = [ membership.group for membership in MemberShip.objects.filter(user=request.user,is_admin=False,is_approved=True) ]
    joined_counter = len(joined_groups)
    paginator = ExPaginator(Group.objects.all().order_by('-create_date'),5)
    try:
        page = int(request.GET.get('page'))
    except (ValueError, TypeError):
        page = 1
        top_group, top_group_members, top_group_display = get_top_group()
    try:
        groups = paginator.page(page)
    except (EmptyPage, InvalidPage):
        groups = paginator.page(paginator.num_pages)
    for group in groups.object_list:
        group.members_count = MemberShip.objects.filter(group=group).count()
    return render_to_response('groups/frontpage.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/login/')
def single(request,group_slug):
    group = get_object_or_404(Group,slug=group_slug)
    friend_groups = group.friend_groups.all().order_by('?')[:8]
    members = [ membership.user for membership in MemberShip.objects.filter(group=group,is_approved=True).order_by('?')[0:7] ]
    member_counter = MemberShip.objects.filter(group=group,is_approved=True).count()
    activities = Activity.objects.filter(host_groups=group)
    activities_count = activities.count()
    co_activities_count = HostShip.objects.filter(group=group,accepted=True).annotate(host_groups_count=Count('activity__host_groups')).filter(host_groups_count__gt=1).count()
    last_activities = activities[:4]
    try:
        membership = MemberShip.objects.get(user=request.user,group=group)
    except MemberShip.DoesNotExist:
        is_admin, is_member, is_approved = False,False,False
    else:
        is_member = True
        is_admin = membership.is_admin
        is_approved = membership.is_approved
    return render_to_response('groups/single.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/login/')
def random(request):
    group = Group.objects.order_by('?')[0]
    return redirect('/groups/%s' % group.slug)

def group_inform(group,user):
    subject = u"[组织]"+ group.name + u" 邀请您加入"
    t = get_template('groups/inform.html')
    body = t.render(Context({'group':group}))
    inform(subject,body,user)

@login_required(login_url='/login/')
def new(request):
    if request.POST:
        form = NewGroupForm(request.POST)
        success,group,membership=form.create_group(request.user)
        if success:
            for user_id in form.cleaned_data['inform_users']:         
                group_inform(group,User.objects.get(pk=user_id))
        return redirect('/groups/%s' % group.slug)
    else:
        form=NewGroupForm()
    return render_to_response('groups/new.html', {
        'form':form
        }, context_instance=RequestContext(request)
    )

@login_required(login_url='/login/')
def admin(request,group_slug):
    group = get_object_or_404(Group,slug=group_slug)
    current_filter = request.GET.get('filter','all')
    filters = {
        'unapproved':u'未审核',
        'single':u'组织活动',
        'multiple':u'合作活动',
        'all':u'全部活动',
    }
    if current_filter not in filters:
        current_filter = 'all'
    current_filter_name = filters[current_filter]
    current_filter_query = u'&filter=' + current_filter
    if current_filter == 'unapproved':
        hostships = HostShip.objects.filter(group=group,accepted=False)
    elif current_filter == 'single':
        hostships =  [ hostship for hostship in HostShip.objects.filter(group=group,accepted=True).annotate(Count('activity__host_groups')) if hostship.activity__host_groups__count == 1 ]
    elif current_filter == 'multiple':
        hostships =  [ hostship for hostship in HostShip.objects.filter(group=group,accepted=True).annotate(Count('activity__host_groups')) if hostship.activity__host_groups__count > 1 ]
    else:
        hostships = HostShip.objects.filter(group=group)
    friend_groups = group.friend_groups.all()
    friend_groups_pk =  [ friend_group.pk for friend_group in friend_groups ]
    friend_groups_pk_str = ','.join([ str(pk) for pk in friend_groups_pk])+','
    admins = [ membership.user for membership in MemberShip.objects.filter(group=group,is_admin=1) ]
    memberships = MemberShip.objects.filter(group=group).exclude(user=request.user).order_by('-joined_date')[0:4]
    is_founder = group.founder.pk == request.user.pk
    paginator = ExPaginator(hostships,5)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        hostships = paginator.page(page)
    except (EmptyPage, InvalidPage):
        hostships = paginator.page(paginator.num_pages)
    if request.POST:
        form = AdminGroupForm(request.POST,instance=group)
        if form.is_valid():
            form.save()
            new_friends = set(form.cleaned_data['friend_groups'])
            for to_remove in set(friend_groups_pk) - new_friends:
                group.friend_groups.remove(Group.objects.get(id=to_remove))
            for to_add in new_friends - set(friend_groups_pk):
                group.friend_groups.add(Group.objects.get(id=to_add))
    else:
        form = AdminGroupForm(instance=group)
    return render_to_response('groups/admin.html',locals(),context_instance=RequestContext(request))

@login_required(login_url='/login/')
def members(request,group_slug):
    group = get_object_or_404(Group,slug=group_slug)
    friend_groups = group.friend_groups.all().order_by('?')[:8]
    paginator = ExPaginator([ membership.user for membership in MemberShip.objects.filter(group=group,is_admin=0,is_approved=True) ],10)
    admins = [ membership.user for membership in MemberShip.objects.filter(group=group,is_admin=1) ]
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1   
    try:
        members = paginator.page(page)
    except (EmptyPage, InvalidPage):
        members = paginator.page(paginator.num_pages)
    is_admin = request.user in admins
    return render_to_response('groups/members.html',locals(), context_instance=RequestContext(request))

@login_required
def my(request):
    paginator = ExPaginator([ membership.group for membership in MemberShip.objects.filter(user=request.user) ],10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        groups = paginator.page(page)
    except (EmptyPage, InvalidPage):
        groups = paginator.page(paginator.num_pages)
    for group in groups.object_list:
        group.members_count = MemberShip.objects.filter(group=group).count()
    return render_to_response('groups/my.html',locals(), context_instance=RequestContext(request))

@login_required
def exit(request,group_slug):
    group = get_object_or_404(Group,slug=group_slug)
    if request.user.pk == group.founder.pk:
        return redirect('/groups/%s' % group.slug )
    else:
        try:
            MemberShip.objects.get(user=request.user,group=group).delete()
        except ObjectDoesNotExist:
            pass
        return redirect('/groups/')

@login_required
def disband(request,group_slug):
    group = Group.objects.get(slug=group_slug)
    if not request.user.pk == group.founder.pk:
        return HttpResponseForbidden()
    else:
        MemberShip.objects.filter(group=group).delete()
        group.delete()
        return redirect('/groups/')