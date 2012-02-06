from django.db import models
from django.contrib.auth.models import User
from NearsideBindings.group.models import Group

class Location(models.Model):
    name = models.CharField(max_length=30,unique=True)
    parent = models.ForeignKey('Location',default=0)
    def __unicode__(self):
        return self.name

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
    participators = models.ManyToManyField(User, related_name='participators')
    hosts = models.ManyToManyField(User, related_name='hosts')
    host_groups = models.ManyToManyField(Group, through='HostShip')
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

class HostShip(models.Model):
   """hostship between group and Activity"""
   group = models.ForeignKey(Group)
   activity = models.ForeignKey(Activity)
   accepted = models.BooleanField(default=False)
