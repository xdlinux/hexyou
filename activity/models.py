from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
	name = models.CharField(max_length=30)

class Activity(models.Model):
	name = models.CharField(max_length=30)
	date = models.DateField()
	begin_time = models.TimeField()
	end_time = models.TimeField()
	description = models.TextField(null=True, blank=True)
	location = models.ForeignKey(Location)
	host = models.ForeignKey(User)
    host_group = models.ForeignKey(Group,null=True)
	participator = models.ManyToManyField(User)

