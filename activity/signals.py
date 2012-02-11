# -*- coding: utf-8 -*-  
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import get_template
from messages.models import Message
from NearsideBindings.group.models import Group
from NearsideBindings.activity.settings import *
from django.template import Context

def inform(subject,body,recipient):
    new_msg = Message(subject=subject,body=body,sender=User.objects.get(pk=0),recipient=recipient)
    new_msg.save()

def activity_inform(sender,**kwargs):
    if not kwargs['instance'].accepted:
        return
    subject = u"[活动]"+ kwargs['instance'].activity.title + u" " + kwargs['instance'].activity.get_host_string(False)
    t = get_template('activities/create_inform.html')
    body = t.render(Context({'activity':kwargs['instance'].activity}))
    for member in kwargs['instance'].group.members.all():
           inform(subject,body,member)