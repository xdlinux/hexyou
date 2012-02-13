import os, ImageFile, md5, time, urllib, hashlib
from django.core.serializers import json, serialize
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson
from messages.models import Message
from NearsideBindings.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib.auth.models import User

class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                object, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')

class AjaxForbidden(Exception):
    pass

class ExPaginator(Paginator):
    def page(self,number):
        self._slice_start = (number/self.per_page)*self.per_page
        self._slice_end = (number/self.per_page+1)*self.per_page
        self.page_range_slice = self.page_range[self._slice_start:self._slice_end]
        return super(ExPaginator,self).page(number)

def upload_image(request_file):
    parser = ImageFile.Parser()
    for chunk in request_file:
        parser.feed(chunk)
    img = parser.close()
    filename = md5.new(str(time.time())).hexdigest()
    if img.format == 'JPEG':
        ext = '.jpg'
    else:
        ext = '.' + img.format.lower()
    filename = filename + ext
    path = os.path.join(MEDIA_ROOT,'tmp')
    if not os.path.isdir(path):
        os.mkdir(path)
    img.save(os.path.join(path,filename))
    return os.path.join(MEDIA_URL,'tmp',filename)

def get_gravatar_url(email,size=150):
    default = "http://localhost/static/images/no_avatar.png"
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url

def small_avatar(entity):
    split = entity.avatar.split('.')
    return '.'.join(split[:-1])+'_small.'+split[-1]

def timebaseslug():
    return md5.new(str(time.time())).hexdigest()

def inform(subject,body,recipient):
    new_msg = Message(subject=subject,body=body,sender=User.objects.get(pk=0),recipient=recipient)
    new_msg.save()