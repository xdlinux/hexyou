# -*- coding: utf-8 -*-  
from django import template
from django.utils.safestring import mark_safe
import re
register=template.Library()

@register.filter
def holding(holding,holder):
    s="<div class='holding'>\n%s\n<span class='holder'>%s</span>\n</div>"% (holding,holder)
    return mark_safe(s)

@register.filter
def prepend(content,prepend):
    args=prepend.split('|')
    if len(args)==1:
        return mark_safe("<div class='input-prepend'>\n<span class='add-on'>%s</span>\n%s\n</div>"%(args[0],str(content).decode('utf-8')))
    else:
        return mark_safe(u"<div class='input-prepend holding'>\n<span class='add-on'>%s</span>\n%s\n<span class='holder'>%s</span>\n</div>"%(args[0],content,args[1]))

@register.filter
def label(field,label):
    s="<div class='clearfix'>\n<label for='%s'>%s</label>\n<div class='input'>%s</div>\n</div>" % (field.auto_id, label, field)
    return mark_safe(s)

