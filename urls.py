from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from NearsideBindings.base.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NearsideBindings.views.home', name='home'),
    # url(r'^NearsideBindings/', include('NearsideBindings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^/?$',index),
    url(r'^home/?$','NearsideBindings.base.views.home'),
    url(r'^signup/?$',signup),
    url(r'^login/?$',login),
    url(r'^logout/?$',logout),
    url(r'^activities/?$','NearsideBindings.activity.views.frontpage'),
    url(r'^activities/single/$','NearsideBindings.activity.views.single'),
    url(r'^activities/create/?$','NearsideBindings.activity.views.create'),
    url(r'^profile/?$','NearsideBindings.member.views.profile'),
    url(r'^profile/edit/?$','NearsideBindings.member.views.edit_profile'),
    url(r'^members/?$','NearsideBindings.member.views.frontpage'),
    url(r'^members/(\w[a-zA-Z0-9_]{1,20})/?$','NearsideBindings.member.views.single'),
    url(r'^groups/?$','NearsideBindings.group.views.frontpage'),
    url(r'^groups/new/?$','NearsideBindings.group.views.new'),
    url(r'^groups/random/?$','NearsideBindings.group.views.random'),
    url(r'^groups/(\w{1,50})/?$','NearsideBindings.group.views.single'),
    url(r'^groups/(\w{1,50})/admin/?$','NearsideBindings.group.views.admin'),
    url(r'^groups/(\w{1,50})/members/?$','NearsideBindings.group.views.members'),
    url(r'^help/?$','NearsideBindings.base.views.help'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^upload/?$',upload),
     url(r'^crop/(\w+)/?$',crop),
     url(r'^json/?$',json)
)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
