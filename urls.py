__author__ = 'lennin'

from django.conf.urls import *

from video_sharing.views import category_view, video_view

urlpatterns = patterns('',
    url(r'category/(?P<category>\w+)/$', category_view, name='category-archive'),
    url(r'video/(?P<video>\w+)/$', video_view, name='play-video'),
)