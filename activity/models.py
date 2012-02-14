# -*- coding: utf-8 -*-  
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from NearsideBindings.group.models import Group
from NearsideBindings.activity.signals import activity_inform

class Location(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('Location',null=True,blank=True)
    def __unicode__(self):
        return self.name

    def full_path(self):
        if self.parent:
            return "%s-%s" % (self.parent.full_path(),self.name)
        else: return self.name

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
    participators = models.ManyToManyField(User, related_name='participate_activities')
    hosts = models.ManyToManyField(User, related_name='hosts')
    host_groups = models.ManyToManyField(Group, through='HostShip')
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
        for host in self.hosts.all():
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

class HostShip(models.Model):
   """hostship between group and Activity"""
   group = models.ForeignKey(Group)
   activity = models.ForeignKey(Activity)
   accepted = models.BooleanField(default=False)

#post_save.connect(activity_inform,sender=HostShip)
