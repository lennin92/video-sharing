__author__ = 'lennin'

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from video_sharing import forms, models
from filetransfers.api import serve_file


def video_get(request, video, mime):
    _video = get_object_or_404(models.VideoData, video=video, mimetype=mime)
    return serve_file(request, _video.data, content_type='video/%s'%_video.mimetype)


@login_required()
def upload_video_s1(request):
    context = RequestContext(request)
    if request.method == 'POST':
        video_form = forms.VideoForm(data=request.POST, files=request.FILES)

        if video_form.is_valid():

            # get users information from post request
            video = video_form.save(commit=False)
            video.owner = request.user
            video.generate_id()
            # persist video object
            if 'thumbnail' in request.FILES:
                video.thumbnail = request.FILES['thumbnail']
            video.save()

            # redirect to login
            return HttpResponseRedirect(reverse('upload-video-step2',kwargs={'video':video.video_id}))
        else:
            return render_to_response('videos/add-video-step1',
                {
                    'video_form': video_form,
                    'has_errors': True,
                    'video_form_errors':  video_form.errors,
                }, context)

    elif request.method == 'GET':
        video_form = forms.VideoForm()
        return render_to_response('videos/add-video-step1',
            {
                'video_form': video_form,
                'has_errors': False
            }, context)
    else:
        return HttpResponseNotAllowed()

@login_required(redirect_field_name='login')
def upload_video_s2(request, video):
    context = RequestContext(request)
    if request.method == 'POST':
        video_form = forms.VideoDataForm(data=request.POST, files=request.FILES)

        if video_form.is_valid():

            # get users information from post request
            _video = video_form.save(commit=False)
            _video.video = models.Video.objects.get(pk=video)
            _video.save()

            # redirect to login
            return HttpResponseRedirect(reverse('play-video',kwargs={'video':video}))
        else:
            print (video_form.errors)
            return render_to_response('videos/add-video-step1',
                {
                    'video_form': video_form,
                    'has_errors': True,
                    'video_form_errors':  video_form.errors,
                }, context)

    elif request.method == 'GET':
        video_form = forms.VideoDataForm()
        return render_to_response('videos/add-video-step2',
            {
                'video_form': video_form,
                'has_errors': False
            }, context)
    else:
        return HttpResponseNotAllowed()
