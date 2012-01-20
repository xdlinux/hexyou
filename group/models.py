from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Condition(models.Model):
    title = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return self.title

class GroupType(models.Model):
    title = models.CharField(max_length=20)
    def __unicode__(self):
        return self.title

class Group(models.Model):
    """Group"""
    name = models.CharField(max_length=20,unique=True)
    founder = models.ForeignKey(User,related_name='founder')
    members = models.ManyToManyField(User,related_name='members',through='MemberShip')
    create_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    condition = models.ForeignKey(Condition,default=1)
    group_type = models.ForeignKey(GroupType,default=1)
    avatar = models.CharField(max_length=512,default='/static/images/group_default.jpg')
    def __unicode__(self):
        return self.name
    
    

class MemberShip(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

