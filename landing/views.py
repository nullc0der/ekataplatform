import json
import os

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User

from utils import send_contact_email

from landing.models import News, Tags, HashtagImg, OgTag


# Create your views here.


def index_page(request):
    try:
        ogtag = OgTag.objects.get(page='index')
    except ObjectDoesNotExist:
        ogtag = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        send_contact_email(
            email=email,
            name=name,
            subject=subject,
            message=message
        )
    return render(
        request,
        'landing/index.html',
        {
            'ogtag': ogtag
        }
    )


def hashtag_page(request):
    hashtagimges = HashtagImg.objects.all()
    try:
        ogtag = OgTag.objects.get(page='hashtag')
    except ObjectDoesNotExist:
        ogtag = None
    return render(
        request,
        'landing/hashtag.html',
        {
            'hashtagimges': hashtagimges,
            'ogtag': ogtag
        }
    )


def getimage(request):
    id = request.GET.get('id')
    hashtag = HashtagImg.objects.get(id=id)
    data = json.dumps({
        'uploader': hashtag.uploader,
        'img': hashtag.image.url
    })
    content_type = 'application/json'
    return HttpResponse(data, content_type)


def news_page(request):
    newses = News.objects.filter(draft=False).order_by('-id')
    trending = newses.order_by('-clickcount')
    try:
        ogtag = OgTag.objects.get(page='news')
    except ObjectDoesNotExist:
        ogtag = None
    if trending:
        trending = trending[:3]
    else:
        trending = None
    if 'tag' in request.GET:
        tag = request.GET.get('tag')
        tag = Tags.objects.get(name=tag)
        newses = newses.filter(tags=tag)
    if 'author' in request.GET:
        author = request.GET.get('author')
        author = User.objects.get(username=author)
        newses = newses.filter(author=author)
    return render(
        request,
        'landing/news.html',
        {
            'newses': newses,
            'trending': trending,
            'tags': Tags.objects.all(),
            'ogtag': ogtag
        }
    )


def news_detail_page(request, id):
    news = News.objects.get(id=id)
    news.clickcount += 1
    news.save()
    if hasattr(news, 'newsogtag'):
        ogtag = news.newsogtag
    else:
        ogtag = None
    return render(
        request,
        'landing/newsdetail.html',
        {
            'news': news,
            'ogtag': ogtag
        }
    )
