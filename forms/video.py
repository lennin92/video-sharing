__author__ = 'lennin'

from django.forms  import ModelForm
from video_sharing.models import Video, VideoData, Comment


class VideoForm(ModelForm):
    class Meta:
        model = Video
        exclude = ['publish_date','modified_date', 'video_id', 'owner']


class VideoDataForm(ModelForm):
    class Meta:
        model = VideoData
        exclude = ['video']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['publish_date','modified_date',
                   'author' , 'parent_comment']