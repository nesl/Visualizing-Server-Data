from django.conf.urls.defaults import *

urlpatterns = patterns('power.views',
    (r'^$', 'index'),
    (r'^(?P<field>\w+)/(?P<field_val>\d+)/results/$', 'results'),
    (r'^(?P<field>\w+)/(?P<field_val>\w+)/results/$', 'results'),
    (r'^(?P<field>\w+)/(?P<field_val>\d+)/data', 'get_data'),
    (r'^(?P<field>\w+)/(?P<field_val>\w+)/data', 'get_data'),
    ('results/$', 'posted_results'),
)
