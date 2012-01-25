from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson
from NearsideBindings.settings import MEDIA_ROOT, MEDIA_URL
import os, ImageFile, md5, time, urllib, hashlib

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

def get_gravatar_url(email):
    default = "/static/images/no_avatar.png"
    size = 150
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url

def timebaseslug():
    return md5.new(str(time.time())).hexdigest()