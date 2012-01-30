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
    slug = models.SlugField(unique=True)
    avatar = models.CharField(max_length=100,default='/static/images/no_avatar.png')
    activity_type = models.ForeignKey(ActivityType,default=1)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True,null=True)
    location = models.ForeignKey(Location)
    participators = models.ManyToManyField(User, related_name='participators')
    hosts = models.ManyToManyField(User, related_name='hosts')
    host_groups = models.ManyToManyField(Group)

