# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from core import views, forms

urlpatterns = patterns('',
    
    url(r'^$', views.main, name='main'),
    url(r'^search', views.search, name='search'),
    
    url(r'^register', forms.RegistrationForm.as_view(), name='register'),
    url(r'^login', forms.LoginForm.as_view(), name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^profile$', views.profile_redirect, name='profile_redirect'),
    url(r'^profile/(?P<username>.+)$', views.profile, name='profile'),
    
    url(r'^detailed/id(?P<post_id>\d+)$', views.detailed, name='detailed'),
    
    url(r'^new$', views.new_redirect, name='new_redirect'),
    url(r'^new/(?P<username>.+)$', views.new_post, name='new_post'),
     
)

    
