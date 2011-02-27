from django.conf.urls.defaults import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^user/$', 'count.views.user'),
    (r'^spreadsheets/$', 'count.views.spreadsheets'),
    (r'^count/$', 'count.views.index'),
    (r'^count/(?P<count_id>\d+)/$', 'count.views.detail'),
    (r'^count/(?P<count_id>\d+)/results/$', 'count.views.results'),
    (r'^count/(?P<count_id>\d+)/vote/$', 'count.views.vote'),
    (r'^admin/', include(admin.site.urls)),
    # Example:
    # (r'^owords/', include('owords.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
