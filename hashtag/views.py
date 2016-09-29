import os
import json
import tempfile
import requests
import tweepy

from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2

from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialApp

from profilesystem.models import UserDocuments
from landing.models import HashtagImg

# Create your views here.
IMAGE_EXTENSION = ['jpg', 'png', 'gif']


@login_required
def get_facebook_account(request):
    if request.method == 'POST':
        social_accounts = request.user.socialaccount_set.all()
        user_has_facebook = False
        response_dict = {}
        for social_account in social_accounts:
            if social_account.get_provider_display() == 'Facebook':
                user_has_facebook = True
                account = social_account
                break
        if user_has_facebook:
            response_dict['has_facebook'] = True
            req = requests.get(account.get_avatar_url())
            response_dict['avatar_url'] = req.url
            tokens = SocialToken.objects.filter(
                account__user=request.user,
                account__provider='facebook'
            )
            response_dict['access_token'] = tokens[0].token
            response_dict['uid'] = account.uid
        else:
            response_dict['has_facebook'] = False
        data = json.dumps(response_dict)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        return HttpResponseForbidden()


@login_required
def get_twitter_account(request):
    if request.method == 'POST':
        social_accounts = request.user.socialaccount_set.all()
        user_has_twitter = False
        response_dict = {}
        for social_account in social_accounts:
            if social_account.get_provider_display() == 'Twitter':
                user_has_twitter = True
                break
        if user_has_twitter:
            response_dict['has_twitter'] = True
            twitter = SocialApp.objects.get(name='twitter')
            tokens = SocialToken.objects.filter(
                account__user=request.user,
                account__provider='twitter'
            )
            consumer_key = twitter.client_id
            consumer_secret = twitter.secret
            access_token = tokens[0].token
            access_token_secret = tokens[0].token_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            me = api.me()
            response_dict['avatar_url'] = me.profile_image_url_https
        else:
            response_dict['has_twitter'] = False
        data = json.dumps(response_dict)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        return HttpResponseForbidden()


@login_required
def upload_to_twitter(request):
    if request.method == 'POST':
        source = request.FILES.get('source')
        twitter = SocialApp.objects.get(name='twitter')
        tokens = SocialToken.objects.filter(
            account__user=request.user,
            account__provider='twitter'
        )
        consumer_key = twitter.client_id
        consumer_secret = twitter.secret
        access_token = tokens[0].token
        access_token_secret = tokens[0].token_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        f = tempfile.NamedTemporaryFile(
            prefix='twitter',
            suffix='.png',
            delete=False
        )
        f.writelines(source)
        g = GeoIP2()
        latlng = g.lat_lon(get_client_ip(request))
        hashtagimg = HashtagImg()
        hashtagimg.lat = latlng[0]
        hashtagimg.lng = latlng[1]
        hashtagimg.uploader = request.user.username
        hashtagimg.image = File(f)
        hashtagimg.save()
        f.close()
        api.update_profile_image(f.name)
        os.remove(f.name)
        return HttpResponse("Ok")
    else:
        return HttpResponseForbidden()


@login_required
def get_images(request):
    image_l = []
    documents = UserDocuments.objects.filter(user=request.user)
    for document in documents:
        a = document.filename().split('.')
        if len(a) > 1:
            if a[1].lower() in IMAGE_EXTENSION:
                image_l.append(document)
    return render(request, 'hashtag/images.html', {'images': image_l})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def save_hashtag(request):
    if request.method == 'POST':
        source = request.FILES.get('source')
        f = tempfile.NamedTemporaryFile(
            suffix='.png',
            delete=False
        )
        f.writelines(source)
        userdoc = UserDocuments(user=request.user)
        userdoc.document = File(f)
        userdoc.save()
        g = GeoIP2()
        latlng = g.lat_lon(get_client_ip(request))
        hashtagimg = HashtagImg()
        hashtagimg.lat = latlng[0]
        hashtagimg.lng = latlng[1]
        hashtagimg.uploader = request.user.username
        hashtagimg.image = File(f)
        hashtagimg.save()
        f.close()
        os.remove(f.name)
    return HttpResponse("OK")
