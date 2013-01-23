# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from django_openid_auth.views import login_begin, login_complete
from django.contrib.auth.views import logout

urlpatterns = patterns('',
        url(r'^login/$', login_begin, name='openid-login'),
        url(r'^complete/$', login_complete, name='openid-complete'),
        url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)
