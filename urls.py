__author__ = 'lennin'

from django.conf.urls import *

from video_sharing.views import category_view, video_view, \
    loginv, upload_video_s1, upload_video_s2, signup, home, video_get

urlpatterns = patterns('',
    url(r'^category/(?P<category>\w+)/$', category_view, name='category-archive'),
    url(r'^video/upload/$', upload_video_s1, name='upload-video'),
    url(r'^video/upload/edit/(?P<video>\w+)/$', upload_video_s2, name='upload-video-step2'),
    url(r'^video/(?P<video>\w+)/$', video_view, name='play-video'),
    url(r'^video/(?P<video>\w+)/get/(?P<mime>\w+)/$', video_get, name='get-video'),
    url(r'^login/$', loginv, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^$', home, name='home'),
)