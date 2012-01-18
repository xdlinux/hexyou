from django.db import models
from django.contrib.auth.models import User
from NearsideBindings.group.models import Group

class Location(models.Model):
    name = models.CharField(max_length=30)

class Activity(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    location = models.ForeignKey(Location)
    participators = models.ManyToManyField(User, related_name='participators')
    hosts = models.ManyToManyField(User, related_name='hosts')
    host_groups = models.ManyToManyField(Group)

