'''
Created on Sep 24, 2014

@author: apple
'''
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = patterns('',
    url(r'^user/$', views.UserView.as_view()),
    url(r'^quote/$', views.QuoteView.as_view()),
)

