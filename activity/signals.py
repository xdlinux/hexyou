# -*- coding: utf-8 -*-  
from django.template.loader import get_template
from django.template import Context
from NearsideBindings.base.utils import inform

def activity_inform(sender,**kwargs):
    if not kwargs['instance'].accepted:
        return
    subject = u"[活动]"+ kwargs['instance'].activity.title + u" " + kwargs['instance'].activity.get_host_string(False)
    t = get_template('activities/create_inform.html')
    body = t.render(Context({'activity':kwargs['instance'].activity}))
    for member in kwargs['instance'].group.members.all():
        inform(subject,body,member)