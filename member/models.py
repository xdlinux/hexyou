# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from datetime import datetime
class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class Profile(object):
    __metaclass__ = ProfileBase

class UserProfile(Profile):
    bio = models.TextField(blank=True)
    site = models.URLField(blank=True)
    avatar = models.CharField(max_length=100,blank=True)
    student_num = models.CharField(max_length=8, blank=True)
    contact_twitter = models.CharField(max_length=32, blank=True)
    contact_qq = models.CharField(max_length=20, blank=True)
    contact_msn = models.EmailField(max_length=75, blank=True)
    contact_fanfou = models.CharField(max_length=75, blank=True)
