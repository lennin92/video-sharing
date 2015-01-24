
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return "Tag %d: %s"%(self.tag_id, self.tag)

    def __unicode__(self):
        return "Tag %d: %s"%(self.tag_id, self.tag)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('category-archive', [self.slug])


class Vote(models.Model):
    LIKE = 0
    DISLIKE= 1

    VOTE_TYPES = ((LIKE,'LIKE'),(DISLIKE,'DISLIKE'))

    author = models.ForeignKey(User)
    type = models.IntegerField(choices=VOTE_TYPES)


class Comment(models.Model):
    author = models.ForeignKey(User)
    comment_text = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self')


def get_video_thumb_upload_dir(i):
    return 'videos/%s/%s/thumb' % (i.video.user.username,
                                    i.video.video_id)


class Video(models.Model):
    video_id = models.CharField(primary_key=True,max_length=50)
    title = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, blank=True)
    is_public = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to=get_video_thumb_upload_dir)

    @models.permalink
    def get_absolute_url(self):
        return ('')


def get_video_data_upload_dir(i):
    return 'videos/%s/%s/%s' % (i.video.user.username,
                                    i.video.video_id,

                                    i.mimetype)
class VideoData(models.Model):
    MP4  = 'mp4'
    OGG  = 'ogv'
    WEBM = 'webm'
    MIMETYPES = (
        (MP4, 'video/mp4'),
        (OGG, 'video/ogg'),
        (WEBM, 'video/webm')
    )
    video = models.ForeignKey(Video)
    mimetype = models.CharField(choices=MIMETYPES,max_length=5)
    is_source = models.BooleanField(default=True)
    data = models.FileField(upload_to=get_video_data_upload_dir)


class PlayList(models.Model):
    playlist_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=254)
    description = models.TextField()
    videos = models.ManyToManyField(Video)
    is_public = models.BooleanField(default=True)


class UserVotesVideo(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)

class UserVotesComment(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)

class UserVotesPlaylist(models.Model):
    user = models.ForeignKey(User)
    playlist = models.ForeignKey(PlayList)

class UserCommentsVideo(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)

class UserCommentsPlaylist(models.Model):
    user = models.ForeignKey(User)
    playlist = models.ForeignKey(PlayList)
