__author__ = 'lennin'

from django.db import models
from django.contrib.auth.models import User
from datetime import date
import hashlib, random, string

def randomStr(minLen, maxLen):
    strLen = random.choice(range(minLen,maxLen))
    return ''.join(random.choice(string.lowercase) for i in range(strLen))


def get_user_profile_pic_upload_dir(i,f):
    return 'user_pics/%s' % i.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User,)
    profile_pic = models.ImageField(blank=True,
                        upload_to=get_user_profile_pic_upload_dir)

    def __str__(self):
        return "User %s"% self.user.username

    def __unicode__(self):
        return "User %s"% self.user.username

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

    def __str__(self):
        return "Category %d: %s"%(self.category_id, self.description)

    def __unicode__(self):
        return "Category %d: %s"%(self.category_id, self.description)

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
    parent_comment = models.ForeignKey('self', blank=True, null=True)

    def get_childs(self):
        print(dir(self))
        return self.comment_set.all()


def get_video_thumb_upload_dir(i,f):
    return 'videos/%s/%s/thumb' % (i.owner.username,
                                    i.video_id)


class Video(models.Model):
    video_id = models.CharField(primary_key=True,max_length=50)
    title = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, blank=True)
    is_public = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to=get_video_thumb_upload_dir)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    #  RANDOM ID FROM 20 TO 50 VARIABLE LENGTH
    def generate_id(self):
        minLen = 15
        maxLen = 46
        valid_lengths = range(minLen, maxLen)
        idLen = random.choice(valid_lengths)
        seed = hashlib.md5(self.title).hexdigest()
        seed += hashlib.md5(self.description).hexdigest()
        seed += hashlib.md5(self.owner.username).hexdigest()
        seed += hashlib.md5(randomStr(minLen,maxLen)).hexdigest()
        last_part = hashlib.sha224(seed).hexdigest()[:idLen]
        today = date.today()
        first_part = hashlib.md5(self.owner.username+str(today.year+today.month)).hexdigest()
        new_id = first_part[:5] + last_part
        self.video_id = new_id.upper()

    def getComments(self):
        userComents = UserCommentsVideo.objects.get(video=self.video_id)
        return [uc.comment for uc in userComents]


def get_video_data_upload_dir(i,f):
    return 'videos/%s/%s/video.%s' % (i.video.owner.username,
                                    i.video_id,
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
    data = models.FileField(upload_to=get_video_data_upload_dir)


class PlayList(models.Model):
    playlist_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=254)
    description = models.TextField()
    videos = models.ManyToManyField(Video)
    is_public = models.BooleanField(default=True)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)


class UserVotesVideo(models.Model):
    vote = models.ForeignKey(Vote)
    video = models.ForeignKey(Video)

class UserVotesComment(models.Model):
    vote = models.ForeignKey(Vote)
    comment = models.ForeignKey(Comment)

class UserVotesPlaylist(models.Model):
    comment = models.ForeignKey(Comment)
    playlist = models.ForeignKey(PlayList)

class UserCommentsVideo(models.Model):
    comment = models.ForeignKey(Comment)
    video = models.ForeignKey(Video)

class UserCommentsPlaylist(models.Model):
    comment = models.ForeignKey(Comment)
    playlist = models.ForeignKey(PlayList)
