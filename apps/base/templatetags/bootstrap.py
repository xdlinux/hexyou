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
    s="<div class='control-group'>\n<label class='control-label' for='%s'>%s</label>\n<div class='controls'>%s" % (field.auto_id, label, field)
    if field.help_text:
        s+="<p class='help-block'>%s</p>" % field.help_text
    s+="</div>\n</div>"
    return mark_safe(s)

@register.filter
def words(text,count):
    if len(text)>count:
        return mark_safe(text[0:count]+'...')
    return mark_safe(text)

@register.filter
def first_p(text):
    pattern = re.compile(r'(<p>([^<]*)<\/p>)?')
    match_text = pattern.match(text).groups()[1]
    if match_text[-1] in (u'.',u'。',u'!',u'！',u'?',u'？',):
        match_text = match_text[:-1] + '...'
    return mark_safe('<p>'+match_text+'</p>')
