# -*- coding: utf-8 -*-  
from django.dispatch import receiver
from django.contrib.auth.models import User
from messages.models import Message
from NearsideBindings.group.models import Group
# from NearsideBindings.activity.models import HostShip

def inform(subject,body,recipient):
    new_msg = Message(subject=subject,body=body,sender=User.objects.get(pk=0),recipient=recipient)
    new_msg.save()

def activity_inform(sender,**kwargs):
    if not kwargs['instance'].accepted:
        return
    subject = u"[活动]"+ kwargs['instance'].activity.title + u" " + kwargs['instance'].activity.get_host_string(False)
    body = u""
    for member in kwargs['instance'].group.members.all():
           inform(subject,body,member)