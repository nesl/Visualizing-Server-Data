from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'register/$', register, name="register"),
)
