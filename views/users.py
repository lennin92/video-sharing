__author__ = 'lennin'

from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from video_sharing import forms
from django.contrib.auth import authenticate, login, logout

def signup(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)

        if user_form.is_valid():

            # get users information from post request
            user = user_form.save()
            user.set_password(user.password)
            # persist users object
            user.save()

            # redirect to login
            return HttpResponseRedirect(reverse('login'))
        else:
            return render_to_response('users/signup',
                {
                    'user_form': user_form,
                    'has_errors': True,
                    'user_form_errors':  user_form.errors
                }, context)

    elif request.method == 'GET':
        user_form = forms.UserForm()
        return render_to_response('users/signup',
            {
                'user_form': user_form,
                'has_errors': False
            }, context)
    else:
        return HttpResponseNotAllowed()


def loginv(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # verify authentication of credentials
        user = authenticate(username=username, password=password)

        if user:
            # if is a valid try to login
            if user.is_active:
                # if users is active login and redirect to home
                login(request,user)
                if 'next' in request.GET:
                    red = request.GET['next']
                else:
                    red = reverse('home')
                return HttpResponseRedirect(red)
            else:
                # if users is not active print login screen with errors
                return render_to_response('users/login',
                    {
                        'has_errors': True,
                        'login_error':  "your account is disabled",
                    }, context)
        else:
            return render_to_response('users/login',
                {
                    'has_errors': True,
                    'login_error':  "Invalid credentials",
                }, context)

    elif request.method == 'GET':
        return render_to_response('users/login', context)
    else:
        return HttpResponseNotAllowed()

def logoutv(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))