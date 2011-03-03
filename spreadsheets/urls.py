from django.conf.urls.defaults import *

urlpatterns = patterns('spreadsheets.views',
    (r'^$', 'spreadsheets'),
    (r'^login/$', 'login'),
    url(r'^spreadsheet/(?P<spreadsheet_id>\d+)/$', 'spreadsheet', name='spreadsheet'),
    url(r'^spreadsheet/(?P<spreadsheet_id>\d+)/worksheet/(?P<worksheet_id>\d+)/$', 'worksheet', name='worksheet'),
    url(r'^spreadsheet/(?P<spreadsheet_id>\d+)/worksheet/(?P<worksheet_id>\d+)/column/(?P<column>\w+)/$',
      'count', name='count'),
)

