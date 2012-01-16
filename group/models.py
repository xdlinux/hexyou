from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Group(models.Model):
    """Group"""
    name = models.CharField(max_length=20)
    founder = models.ForeignKey(User,related_name='founder')
    admins = models.ManyToManyField(User,related_name='admins')
    members = models.ManyToManyField(User,related_name='members')
    since = models.DateField(default=date.today())
    description = models.TextField(null=True, blank=True)