from django.conf.urls.defaults import *
from django.contrib.auth.views import logout
from views import *

urlpatterns = patterns('',
    url(r'register/$', register, name="register"),
    url(r'logout/$', logout, name="logout"),
    url(r'activate/$', activate, name="activate"),
)
