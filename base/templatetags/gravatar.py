### gravatar.py ###############
### place inside a 'templatetags' directory inside the top level of a Django app (not project, must be inside an app)
### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %} >
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below

from django import template
from NearsideBindings.base.utils import get_gravatar_url

register = template.Library()

class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        return get_gravatar_url(email)

@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

@register.simple_tag
def avatar(user):
    return user.avatar or get_gravatar_url(user.email,150)

@register.simple_tag
def small_avatar(user):
    if user.avatar:
        split = user.avatar.split('.')
        return '.'.join(split[:-1])+'_small.'+split[-1]
    else:
        return get_gravatar_url(user.email,20)