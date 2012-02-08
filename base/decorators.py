from django.utils import simplejson
from django.contrib.auth.models import User
from NearsideBindings.group.models import MemberShip
from NearsideBindings.base.utils import AjaxForbidden

def json_request(func):
    """ Pre-parse JSON phrase"""
    def wrapper(request,request_phrase):
        return func(request,simplejson.loads(request_phrase))
    return wrapper

def group_admin_required(func):
    def wrapper(request,request_phrase):
        if not MemberShip.objects.only('is_admin').get(group__slug=request_phrase['group'],user=request.user).is_admin:
            raise AjaxForbidden
        return func(request,request_phrase)
    return wrapper