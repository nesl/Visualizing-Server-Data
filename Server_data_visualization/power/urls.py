from django.conf.urls.defaults import *

urlpatterns = patterns('power.views',
    (r'^$', 'charts_menu'),
    (r'^(?P<field>\w+)/(?P<field_val>\d+)/results/$', 'results'),
    (r'^(?P<field>\w+)/(?P<field_val>\w+)/results/$', 'results'),
    (r'^(?P<field>\w+)/(?P<field_val>\d+)/data', 'get_data'),
    (r'^(?P<field>\w+)/(?P<field_val>\w+)/data', 'get_data'),
    (r'^(?P<field>\w+)/(?P<field_val>\w+)/livedata', 'get_live_data'),
    ('results/$', 'posted_results'),
    (r'^data_channel/0/data$', 'check_results'),
)
