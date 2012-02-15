# -*- coding: utf-8 -*-  
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from NearsideBindings.base.forms import LoginForm,SignupForm,ImageCrop,ImageUpload, AjaxStandard
from NearsideBindings.base.utils import JsonResponse, upload_image, get_gravatar_url, small_avatar, AjaxForbidden
from NearsideBindings.base.decorators import json_request, group_admin_required
from NearsideBindings.settings import MEDIA_ROOT, MEDIA_URL, IMAGE_SAVE_CHOICES
from NearsideBindings.group.models import Group, MemberShip
from NearsideBindings.activity.models import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from messages.forms import ComposeForm
import Image, os, urllib, md5

def filter_activities_of_user(user):
    """docstring for filter_activities_of_user"""
    acts=user.participated_activities.filter(hostship__accepted=True).order_by('begin_time').filter(begin_time__gte=datetime.now(),begin_time__lte=(datetime.now()+timedelta(7))).all()
    grouped=[]
    if len(acts)>0:
        ct=acts[0].begin_time
        cg=[]
        for a in acts:
            if a.begin_time.year==ct.year and a.begin_time.month==ct.month and a.begin_time.day==ct.day:
                cg.append(a)
            else:
                grouped.append(cg)
                cg=[]
                cg.append(a)
                ct=a.begin_time
        grouped.append(cg)
    return user.participated_activities.count(),grouped

def index(request):
    if request.user.is_authenticated():
        return redirect('/timeline/')
    return render_to_response("index.html",locals(),context_instance=RequestContext(request))

@login_required(login_url='/login/')
def timeline(request):
    activities_count,lately_activities=filter_activities_of_user(request.user)
    try:
        if request.GET and request.GET.has_key('offset'):
            offset=int(request.GET['offset'])
        else: offset=0
    except Exception, e:
        offset=0
    prew_offset=offset-1
    next_offset=offset+1
    activities=Activity.objects.filter(hostship__accepted=True).filter(hostship__group__membership__user=request.user).order_by('-begin_time').distinct()[9*offset:9*offset+10]
    if activities.count()<10:
        next_offset=False
    return render_to_response("timeline/timeline.html",locals(), context_instance=RequestContext(request))

def signup(request):
    if request.method=="POST" and (not request.POST.has_key('from_mainpage')):
        form=SignupForm(request.POST)
        print form.errors
        if form.is_valid():
            new_user=form.save()
            login_user=auth.authenticate(username=new_user.username,password=request.POST['password1'])
            auth.login(request,login_user)
            return redirect('/members/%s/' % new_user.username)
    else:
        form=SignupForm()
        for name in ['last_name','email','student_num']:
            if request.POST.has_key(name):
                form.fields[name].widget.attrs['value']=request.POST[name]
    return render_to_response("accounts/signup.html",{'form':form},context_instance=RequestContext(request))


def login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user!=None:
                auth.login(request,user)
                if request.GET and request.GET.has_key('next'):
                    return redirect(request.GET['next'])
                return redirect('/members/%s/' % user.username)
            else:
                return render_to_response('accounts/login.html',context_instance=RequestContext(request))
    else: form=LoginForm()
    return render_to_response('accounts/login.html',{'form':form},context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_exempt
def upload(request):
    if request.method == "POST":
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            rlpath,size = upload_image(request.FILES['Filedata'],form.cleaned_data['save_to'])
            if rlpath:
                return JsonResponse({'path':rlpath,'width':size[0],'height':size[1]})
            else:
                return HttpResponseServerError('Uploading error')
        else:
            return HttpResponseBadRequest('Invalid content')
    else:
        return HttpResponseBadRequest()

def crop(request,save_to):
    if request.method == "POST" and save_to in IMAGE_SAVE_CHOICES:
        form = ImageCrop(request.POST)
        if form.is_valid():
            now = datetime.now()
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            w = form.cleaned_data['w']
            h = form.cleaned_data['h']
            cw = form.cleaned_data['cw']
            ch = form.cleaned_data['ch']
            path = form.cleaned_data['path']
            filename = os.path.basename(path)
            abs_path = os.path.join(MEDIA_ROOT,'tmp',os.path.basename(path))
            img = Image.open(abs_path)
            rw = img.size[0]
            rh = img.size[1]
            x_rate = float(rw)/float(cw)
            y_rate = float(rh)/float(ch)
            x1 = int(round(x_rate*x))
            y1 = int(round(y_rate*y))
            x2 = int(round(x_rate*(x+w)))
            y2 = int(round(y_rate*(y+h)))
            box = (x1,y1,x2,y2)
            crop = img.crop(box)
            size = 150,150
            crop = crop.resize(size,Image.ANTIALIAS)
            base_path=os.path.join(MEDIA_ROOT,save_to)
            if not os.path.isdir(base_path):
                os.mkdir(base_path)
            date = now.strftime('%Y%m')
            date_path=os.path.join(base_path,date)
            if not os.path.isdir(date_path):
                os.mkdir(date_path)
            full_path = os.path.join(date_path,filename)
            small = crop.copy()
            crop.save(full_path)
            small_size = 20,20
            small.thumbnail(small_size,Image.ANTIALIAS)
            split = full_path.split('.')
            small_fname = '.'.join(split[:-1]) + '_small.' + split[-1]
            small.save(small_fname)
            os.remove(abs_path)
            return JsonResponse({'path':os.path.join(MEDIA_URL,save_to,date,filename)})
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseForbidden()

def get_users(request,request_phrase):
    users = User.objects.filter(username__contains=request_phrase).exclude(pk=0).order_by('username')[:5]
    return [{'avatar':small_avatar(user) or get_gravatar_url(user.email,20),'name':user.last_name,'slug':user.username,'category':'user','id':user.id} for user in users]

def get_groups(request,request_phrase):
    groups=Group.objects.filter(Q(slug__contains=request_phrase) | Q(name__contains=request_phrase))[:5]
    return [{'avatar':small_avatar(group),'name':group.name,'slug':group.slug,'category':'group','id':group.id} for group in groups]

def join_group(request,request_phrase):
    group = Group.objects.get(slug=request_phrase)
    if group.condition.pk == 1:
        new_membership = MemberShip(user=request.user,group=group,is_admin=False,is_approved=True)
    elif group.condition.pk == 2:
        new_membership = MemberShip(user=request.user,group=group,is_admin=False,is_approved=False)
    elif group.condition.pk == 3:
        raise AjaxForbidden()
    try:
        new_membership.save()
    except IntegrityError:
        return [{'error':'You have joined this group',},]
    else:
        return [{'condition':group.condition.pk}]

def get_activities(request,request_phrase):
    activities = Activity.objects.filter(title__contains=request_phrase)[:5].values()
    return [{'avatar':activity['avatar'],'name':activity['title'],'slug':"",'category':'activity','id':activity['id']} for activity in activities ]

def get_child_location(request,request_phrase):
    locations = Location.objects.filter(parent=int(request_phrase)) 
    return [{'name':location.name,'id':location.id} for location in locations ]

@json_request
def create_location(request,request_phrase):
    new_location = Location(name=request_phrase['name'],parent=Location.objects.get(id=int(request_phrase['parent'])))
    try:
        new_location.save()
    except IntegrityError:
        raise AjaxForbidden()
    else:
        return ""

@json_request
def get_member(request,request_phrase):
    fwords = lambda s:s[0:50]+"..." if len(s)>50 else s
    if request_phrase['term'] == '*':
        memberships = MemberShip.objects.filter(group__slug=request_phrase['group']).exclude(user=request.user).order_by('-joined_date')
    else:
        memberships = MemberShip.objects.filter(Q(group__slug=request_phrase['group']),Q(user__username__contains=request_phrase['term']) | Q(user__last_name__contains=request_phrase['term'])).exclude(user=request.user).order_by('-joined_date')
    filters = ['all','admin','member','unapproved']
    is_founder =  Group.objects.get(slug=request_phrase['group']).founder.pk == request.user.pk
    if request_phrase['filter'] not in filters:
        raise AjaxForbidden()
    elif request_phrase['filter'] == 'admin':
        memberships= memberships.filter(is_admin=True)
    elif request_phrase['filter'] == 'member':
        memberships = memberships.filter(is_admin=False,is_approved=True)
    elif request_phrase['filter'] == 'unapproved':
        memberships = memberships.filter(is_approved=False)
    memberships = memberships[0:4]
    result = [{'name':membership.user.last_name,'avatar':membership.user.avatar,'slug':membership.user.username,'id':membership.user.id,'is_admin':membership.is_admin,'is_approved':membership.is_approved,'description':fwords(membership.user.bio)} for membership in memberships ]
    digest = md5.new(simplejson.dumps(result)).hexdigest()
    return [{'digest':digest,'data':result,'is_founder':is_founder}]

@json_request
@group_admin_required
def approve_member(request,request_phrase):
    membership = MemberShip.objects.get(group__slug=request_phrase['group'],user__id=int(request_phrase['user']))
    membership.is_approved=True
    membership.save()
    return ""

@json_request
@group_admin_required
def remove_member(request,request_phrase):
    MemberShip.objects.get(group__slug=request_phrase['group'],user__id=int(request_phrase['user'])).delete()
    return ""

@json_request
def grant_admin(request,request_phrase):
    group = Group.objects.get(slug=request_phrase['group'])
    if not request.user.pk == group.founder.pk:
        raise AjaxForbidden
    membership = MemberShip.objects.get(group=group,user__id=int(request_phrase['user']))
    membership.is_approved=True
    membership.is_admin=True
    membership.save()
    return ""

@json_request
def revoke_admin(request,request_phrase):
    group = Group.objects.get(slug=request_phrase['group'])
    if not request.user.pk == group.founder.pk:
        raise AjaxForbidden
    membership = MemberShip.objects.get(group__slug=request_phrase['group'],user__id=int(request_phrase['user']))
    membership.is_admin=False
    membership.save()
    return ""

@json_request
def send_message(request,request_phrase):
    form = ComposeForm(request_phrase)
    if form.is_valid():
        form.save(sender=request.user)
        return ""
    else:
        raise AjaxForbidden

@json_request
@group_admin_required
def accept_activity(request,request_phrase):
    hostship = HostShip.objects.get(group__slug=request_phrase['group'],activity__id=request_phrase['activity'])
    hostship.accepted = True
    hostship.save()
    return ""

def participate_activity(request,request_phrase):
    memberhostship = MemberHostShip(user=request.user,activity=Activity.objects.get(pk=int(request_phrase)),is_host=False)
    memberhostship.save()
    return ""

@json_request
def save_activity_photos(request,request_phrase):
    activity = Activity.objects.get(id=int(request_phrase['activity']))
    try:
        MemberHostShip.objects.get(user=request.user,activity=activity)
    except MemberHostShip.DoesNotExist:
        raise AjaxForbidden
    for photo in request_phrase['photos']:
        activity.photos.create(source=photo['src'],description=photo['description'])
    return ""

""" Callback swtich string | Callback list | Login requied """
REQUEST_TYPES = (
    ('all',[get_users,get_groups],False),
    ('user',[get_users,],False,),
    ('group',[get_groups,],False,),
    ('activity',[get_activities,],False,),
    ('join_group',[join_group,],True),
    ('location',[get_child_location,],False),
    ('create_location',[create_location,],False),
    ('member',[get_member,],True),
    ('remove_member',[remove_member,],True),
    ('grant_admin',[grant_admin,],True),
    ('revoke_admin',[revoke_admin,],True),
    ('approve_member',[approve_member,],True),
    ('send_message',[send_message,],True),
    ('accept_activity',[accept_activity,],True),
    ('participate_activity',[participate_activity,],True),
    ('save_activity_photos',[save_activity_photos],True)
)

@csrf_exempt
def json(request):
    if request.method == "POST":
        form = AjaxStandard(request.POST)
        if form.is_valid():
            request_type = form.cleaned_data['request_type']
            request_phrase = form.cleaned_data['request_phrase']
            for val in REQUEST_TYPES:
                if request_type==val[0]:
                    result = []
                    if not (request.user.is_authenticated() or val[2]):
                        return HttpResponseForbidden()
                    for func in val[1]:
                        try:
                            result += func(request,request_phrase)
                        except AjaxForbidden:
                            return HttpResponseForbidden()
                        # except Exception:
                        #     return HttpResponseBadRequest()
            return JsonResponse(result)
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseForbidden()

def help(request):
    return render_to_response('help.html', context_instance=RequestContext(request))
