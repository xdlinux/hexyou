from django.shortcuts import render_to_response
from django.template.loader import get_template
from django import template
from django.template import Context

register=template.Library()

@register.filter
def active(value,arg):
    """decide if this topbar item is active"""
    if value == arg :
        return "active"
    else:
        return ""

@register.filter
def white(value,arg):
  if value==arg:
    return "icon-white"
  else:
    return ""


class TopbarNode(template.Node):
    def __init__(self,ls):
       self.active=ls[1]
       if len(ls)>2:
           self.path=ls[2]
       else:
           self.path=None

    def render(self,context):
        context['topbar']=self.active
        if self.path:
            t=get_template(str(self.path))
        else:
            t=get_template("topbar.html" )
            t.render(context)
        return t.render(context)

@register.tag
def topbar(parser,token):
    ls=token.contents.split(None)
    if len(ls)<2:
        msg = '%r tag requires at least 1 arguments, %d given.' % (token.contents[0], len(ls)-1)
        raise template.TemplateSyntaxError(msg)
    return TopbarNode(ls)
