from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
	name = models.CharField(max_length=30)
	date = models.DateField()
	begin_time = models.TimeField()
	end_time = models.TimeField()
	description = models.TextField(null=True, blank=True)
	location = models.ForeignKey(Location)
	host = models.ForeignKey(User)
	participator = models.ManyToManyField(User)

class Profile(models.Model):
	user = models.OneToOne(User)
	group = models.BooleanField()
	verified = models.BooleanField()

class Location(models.Model):
	name = models.CharField(max_length=30)