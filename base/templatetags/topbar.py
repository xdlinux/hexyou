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


class TopbarNode(template.Node):
    def __init__(self,path,active=None):
       self.path=path
       self.active=active

    def render(self,context):
        context['topbar']=self.active
        t=get_template("%s/topbar.html" % self.path)
        return t.render(context)

@register.tag
def topbar(parser,token):
    ls=token.contents.split(None)
    if len(ls)!=3:
        msg = '%r tag requires 2 arguments, %d given.' % (token.contents[0], len(ls)-1)
        raise template.TemplateSyntaxError(msg)
    return TopbarNode(ls[1],ls[2])
