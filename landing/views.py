import json
import os

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from utils import send_contact_email

from landing.models import News, Tags, HashtagImg, GlobalOgTag, OgTagLink
from invitationsystem.models import Invitation
from invitationsystem.forms import GetInvitationForm
from invitationsystem.tasks import send_notification_to_reviewer


# Create your views here.


def index_page(request):
    index_ogtag = OgTagLink.objects.filter(page='index').order_by('-id')
    default_ogtag = GlobalOgTag.objects.filter(name='default').order_by('-id')
    if index_ogtag:
        ogtag = index_ogtag[0].globalogtag
    elif default_ogtag:
        ogtag = default_ogtag[0]
    else:
        ogtag = None
    return render(
        request,
        'landing/index.html',
        {
            'ogtag': ogtag,
            'form': GetInvitationForm()
        }
    )


def hashtag_page(request):
    hashtagimges = HashtagImg.objects.all()
    hashtag_ogtag = OgTagLink.objects.filter(page='hashtag').order_by('-id')
    default_ogtag = GlobalOgTag.objects.filter(name='default').order_by('-id')
    if hashtag_ogtag:
        ogtag = hashtag_ogtag[0].globalogtag
    elif default_ogtag:
        ogtag = default_ogtag[0]
    else:
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
    news_ogtag = OgTagLink.objects.filter(page='news').order_by('-id')
    default_ogtag = GlobalOgTag.objects.filter(name='default').order_by('-id')
    if news_ogtag:
        ogtag = news_ogtag[0].globalogtag
    elif default_ogtag:
        ogtag = default_ogtag[0]
    else:
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
    if news.ogtag:
        ogtag = news.ogtag
    else:
        default_ogtag = GlobalOgTag.objects.filter(name='default').order_by('-id')
        if default_ogtag:
            ogtag = default_ogtag[0]
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


def author_detail_page(request, username):
    user = get_object_or_404(User, username=username)
    newses = News.objects.filter(draft=False).order_by('-id')
    newses = newses.filter(author=user)
    return render(
        request,
        'landing/authordetails.html',
        {
            'user': user,
            'newses': newses
        }
    )


def send_contact_request(request):
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
        return HttpResponse("Ok")
    else:
        return HttpResponseForbidden()


def get_invitation_key(request):
    if request.method == 'POST':
        form = GetInvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            invitation = Invitation()
            invitation.email = email
            invitation.invitation_id = get_random_string(length=6)
            invitation.save()
            send_notification_to_reviewer.delay(email)
            return HttpResponse("Ok")
        else:
            return render(
                request,
                'landing/getinvitationform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return HttpResponseForbidden()


@csrf_exempt
def get_invitation_key_from_production(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        if api_key == settings.EKATA_INVITATION_APIKEY:
            email = request.POST.get('email')
            invitation = Invitation()
            invitation.email = email
            invitation.invitation_id = get_random_string(length=6)
            invitation.save()
            send_notification_to_reviewer.delay(email)
            return HttpResponse('OK')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()
