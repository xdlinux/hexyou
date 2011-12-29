from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from NearsideBindings.base.views  import *
from NearsideBindings.group.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NearsideBindings.views.home', name='home'),
    # url(r'^NearsideBindings/', include('NearsideBindings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^/?$',index),
    url(r'^signup/?$',signup),
    url(r'^signin/?$',signin),
    url(r'^members/?$','NearsideBindings.member.views.frontpage'),
    url(r'^members/single?$','NearsideBindings.member.views.single'),
    url(r'^groups/?$','NearsideBindings.group.views.frontpage'),
    url(r'^groups/single/?$','NearsideBindings.group.views.single'),
     url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
