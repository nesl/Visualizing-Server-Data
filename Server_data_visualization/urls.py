from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #url(r'^$', direct_to_template, {'template': 'base.html'}, name="index"),
    url(r'^$', login, name="login"),
    # For serving static files: jquery.js and highcharts.js
    (r'power/site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'upload/', 'views.upload_file'),
    (r'power/', include('power.urls')),
    (r'accounts/', include('accounts.urls')),
    (r'admin/', include(admin.site.urls)),
)
