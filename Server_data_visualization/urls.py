from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # For serving static files: jquery.js and highcharts.js
    (r'^power/site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^power/', include('power.urls')),
    (r'^admin/', include(admin.site.urls)),
)
