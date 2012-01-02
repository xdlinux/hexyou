# -*- coding: utf-8 -*-  
from django import template
from django.utils.safestring import mark_safe
register=template.Library()

@register.filter
def holding(holding,holder):
    return mark_safe("<div class='holding'>\n%s\n<span class='holder'>%s</span>\n</div>"%(holding,holder))

@register.filter
def prepend(content,prepend):
    args=prepend.split('|')
    if len(args)==1:
        return mark_safe("<div class='input-prepend'>\n<span class='add-on'>%s</span>\n%s\n</div>"%(args[0],str(content).decode('utf-8')))
    else:
        return mark_safe(u"<div class='input-prepend holding'>\n<span class='add-on'>%s</span>\n%s\n<span class='holder'>%s</span>\n</div>"%(args[0],content,args[1]))

