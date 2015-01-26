# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import video_sharing.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(to='video_sharing.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('playlist_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('is_public', models.BooleanField(default=True)),
                ('publish_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(serialize=False, primary_key=True)),
                ('tag', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCommentsPlaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(to='video_sharing.Comment')),
                ('playlist', models.ForeignKey(to='video_sharing.PlayList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCommentsVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(to='video_sharing.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_pic', models.ImageField(upload_to=video_sharing.models.get_user_profile_pic_upload_dir, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserVotesComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(to='video_sharing.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserVotesPlaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(to='video_sharing.Comment')),
                ('playlist', models.ForeignKey(to='video_sharing.PlayList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserVotesVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('video_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('thumbnail', models.ImageField(upload_to=video_sharing.models.get_video_thumb_upload_dir)),
                ('publish_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(to='video_sharing.Category', blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('tags', models.ManyToManyField(to='video_sharing.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mimetype', models.CharField(max_length=5, choices=[(b'mp4', b'video/mp4'), (b'ogv', b'video/ogg'), (b'webm', b'video/webm')])),
                ('data', models.FileField(upload_to=video_sharing.models.get_video_data_upload_dir)),
                ('video', models.ForeignKey(to='video_sharing.Video')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(0, b'LIKE'), (1, b'DISLIKE')])),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='uservotesvideo',
            name='video',
            field=models.ForeignKey(to='video_sharing.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uservotesvideo',
            name='vote',
            field=models.ForeignKey(to='video_sharing.Vote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uservotescomment',
            name='vote',
            field=models.ForeignKey(to='video_sharing.Vote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercommentsvideo',
            name='video',
            field=models.ForeignKey(to='video_sharing.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(to='video_sharing.Video'),
            preserve_default=True,
        ),
    ]
