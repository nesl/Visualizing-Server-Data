from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from views import *

urlpatterns = patterns('',
    url(r'register/$', register, name="register"),
    url(r'login/$', login, name="login"),
    url(r'logout/$', logout, name="logout"),
    url(r'activate/$', activate, name="activate"),
)
