from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #url(r'^signin$', login, name="login"),
    #url(r'^$', login, name="login"),
    (r'^$', direct_to_template, {'template': 'base.html'}),
    # For serving static files: jquery.js and highcharts.js
    (r'site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (r'upload/', 'views.upload_file'),
    (r'power/', include('power.urls')),
    (r'accounts/', include('accounts.urls')),
    (r'admin/', include(admin.site.urls)),
)
