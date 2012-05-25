from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from base.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^NearsideBindings/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^/?$',index),
    url(r'^timeline/?$','base.views.timeline'),
    url(r'^signup/?$',signup),
    url(r'^login/?$',login),
    url(r'^logout/?$',logout),
    url(r'^activities/?$','activity.views.frontpage'),
    url(r'^activities/(\d+)/$','activity.views.single'),
    url(r'^activities/(\d+)/edit$','activity.views.edit'),
    url(r'^activities/create/?$','activity.views.create'),
    url(r'^activities/my/(\w{1,12})?$','activity.views.my'),
    url(r'^activities/sort/(\w{1,12})/(\d+)?$','activity.views.sort'),
    url(r'^activities/random/?$','activity.views.random'),
    url(r'^profile/?$','member.views.profile'),
    url(r'^profile/edit/?$','member.views.edit_profile'),
    url(r'^members/?$','member.views.frontpage'),
    url(r'^members/(\w[a-zA-Z0-9_]{1,20})/?$','member.views.single'),
    url(r'^groups/?$','group.views.frontpage'),
    url(r'^groups/new/?$','group.views.new'),
    url(r'^groups/random/?$','group.views.random'),
    url(r'^groups/my/?$','group.views.my'),
    url(r'^groups/(\w{1,50})/?$','group.views.single'),
    url(r'^groups/(\w{1,50})/admin/?$','group.views.admin'),
    url(r'^groups/(\w{1,50})/members/?$','group.views.members'),
    url(r'^groups/(\w{1,50})/exit/?$','group.views.exit'),
    url(r'^groups/(\w{1,50})/disband/?$','group.views.disband'),
    url(r'^help/?$','base.views.help'),
    url(r'^messages/', include('messages.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^upload/?$',upload),
     url(r'^crop/(\w+)/?$',crop),
     url(r'^json/?$',json)
)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
