from django.conf.urls.defaults import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^user/$', 'count.views.user'),
    (r'^spreadsheets/$', 'count.views.spreadsheets'),
    (r'^spreadsheet/(?P<spreadsheet_id>\d+)/$', 'count.views.spreadsheet'),
    (r'^spreadsheet/(?P<spreadsheet_id>\d+)/worksheet/(?P<worksheet_id>\d+)/$',
      'count.views.worksheet'),
    (r'^spreadsheet/(?P<spreadsheet_id>\d+)/worksheet/(?P<worksheet_id>\d+)/column/(?P<column>\w+)/$',
      'count.views.count'),
    (r'^admin/', include(admin.site.urls)),
    # Example:
    # (r'^owords/', include('owords.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
