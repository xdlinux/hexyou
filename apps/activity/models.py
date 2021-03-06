# -*- coding: utf-8 -*-  
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from group.models import Group
from activity.signals import *

class Location(models.Model):
    name = models.CharField(max_length=30,unique=True)
    parent = models.ForeignKey('Location',null=True,blank=True)
    full_path = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return self.name

    def save(self):
        super(Location,self).save()
        self.full_path = self.get_full_path()
        super(Location,self).save()

    def get_full_path(self):
        if self.parent:
            return '%s - <a href="/activities/sort/location/%d">%s</a>' % (self.parent.get_full_path(),self.pk,self.name)
        else:
            return '<a href="/activities/sort/location/%d">%s</a>' % (self.pk,self.name)

class ActivityType(models.Model):
    title = models.CharField(max_length=20)
    def __unicode__(self):
        return self.title

class Activity(models.Model):
    title = models.CharField(max_length=30)
    avatar = models.CharField(max_length=100,default='/static/images/no_avatar.png')
    activity_type = models.ForeignKey(ActivityType,default=1)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True,null=True)
    location = models.ForeignKey(Location)
    members = models.ManyToManyField(User,through='MemberHostShip',related_name='participated_activities',blank=True)
    # participators = models.ManyToManyField(User, related_name='participators')
    # hosts = models.ManyToManyField(User, related_name='hosts')
    host_groups = models.ManyToManyField(Group, through='HostShip',blank=True)
    host_string = models.CharField(max_length=100,blank=True,null=True)

    def __unicode__(self):
        return self.title

    def __getattr__( self, name ):
        if name == 'host_string':
            self.host_string = self.get_host_string()
            return self.host_string
        super(Activity, self).__getattr__(name)
    def ask_groups_to_host(self,user,*groups):
        user_groups= set(user.groups.all())
        request_groups= set(groups)
        allowed_groups=user_groups & request_groups
        if not allowed_groups:
            raise Exception('You can only ask groups that you have atended to host an activity!')
        for group in allowed_groups:
            if not isinstance(group,Group):
                raise Exception('You can only ask a group to host an activity, not %s'% type(group) )
            else:
                HostShip.objects.create(group=group,activity=self)
    def accepted_host_groups(self):
        return [hostship.group for hostship in self.hostship_set.filter(accepted=True).all()]
    def get_host_string(self,with_link=True):
        accepted_groups = [ hostship.group for hostship in HostShip.objects.filter(activity=self) if hostship.accepted ]
        fullhostship = []
        for host in self.members.filter(memberhostship__is_host=True):
            real_groups = Group.objects.filter(members=host)
            fullhostship.append({'host':host,'groups':set(accepted_groups) & set(real_groups)})
        host_string = u'by '
        for hostship in fullhostship:
            if with_link:
                host_string += u"<a href='/members/%s'>%s</a>" % (hostship['host'],hostship['host'].last_name)
            else:
                host_string += hostship['host'].last_name
            host_string += u'@'
            for group in hostship['groups']:
                if with_link:
                    host_string +=  u"<a href='/groups/%s'>%s</a>," % (group.slug,group.name)
                else:
                    host_string += group.name + ','
            host_string = host_string[:-1]
            host_string += " "
        return host_string

class ActivityPhoto(models.Model):
    activity = models.ForeignKey(Activity,related_name='photos')
    source = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=128, blank=True)
    def save(self,*arg,**karg):
        print self.source
        if not self.thumbnail:
            self.thumbnail=self.source[:-4]+'_small'+self.source[-4:]
        models.Model.save(self)

class HostShip(models.Model):
    """hostship between group and Activity"""
    group = models.ForeignKey(Group)
    activity = models.ForeignKey(Activity)
    accepted = models.BooleanField(default=False)
    class Meta:
        unique_together = ('group','activity')


class MemberHostShip(models.Model):
    """hostship between member and activity"""
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    is_host = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user','activity')

post_save.connect(update_host_string,sender=HostShip)
post_save.connect(activity_inform,sender=HostShip)
