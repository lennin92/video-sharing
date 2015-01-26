__author__ = 'lennin'

from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from video_sharing import models, forms


def category_view(request, category):
    return HttpResponse("""
    <h1>CATEGORY VIEW</h1>
    <p>
        User data
        %s
    </p>
    """%str(request)
    )


def video_view(request, video):
    v = get_object_or_404(models.Video, video_id=video)
    try:
        v_coments = v.usercommentsvideo_set.all()
    except models.UserCommentsVideo.DoesNotExist:
        v_coments = []
    return render_to_response('videos/view-video',
           {
                'video': v,
                'videos': get_object_or_404(models.VideoData, video=video),
                'comment_form': forms.CommentForm(),
                'comments': [ucv.comment for ucv in v_coments],
           }, RequestContext(request))


def home(request):
    return render_to_response('videos/last-videos',
           {
                'last_videos' : get_list_or_404(models.Video)
           }, RequestContext(request))