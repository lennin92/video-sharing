__author__ = 'lennin'

from django.forms  import ModelForm, CharField, PasswordInput
from django.contrib.auth.models import User
from video_sharing.models import UserProfile


class UserForm(ModelForm):

    password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password',
                  'first_name', 'last_name']


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_pic']