import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.contrib.auth.models import User

from channels import Group

from messagingsystem.models import ChatRoom, Message
from useraccount.forms import TransactionForm, RequestForm

# Create your views here.


@login_required
def messaging_index(request):
    chats = ChatRoom.objects.filter(
        subscribers=request.user
    ).order_by('-date_created')
    if 'username' in request.GET:
        username = request.GET.get('username')
        if username:
            chats = chats.filter(
                subscribers__username__istartswith=username
            )
    if chats:
        messages = chats[0].messages.all().order_by('timestamp')
        chat_id = chats[0].id
        for subscriber in chats[0].subscribers.all():
            if subscriber != request.user:
                otheruser = subscriber
    else:
        messages = None
        chat_id = None
        otheruser = None
    if 'navbar' in request.GET:
        has_unread = request.user.recieved_messages.filter(
            read=False
        ).count()
        template = loader.get_template('messagingsystem/navbarmessage.html')
        context = {'chats': chats, 'ruser': request.user}
        m = template.render(context)
        data = {
            'has_unread': has_unread,
            'html': m
        }
        json_data = json.dumps(data)
        mimetype = 'application/json'
        return HttpResponse(json_data, mimetype)
    if 'username' in request.GET:
        return render(
            request,
            'messagingsystem/rooms.html',
            {
                'chats': chats
            }
        )
    return render(
        request,
        'messagingsystem/index.html',
        {
            'chat_id': chat_id,
            'chats': chats,
            'messages': messages,
            'modals': True,
            'otheruser': otheruser,
            'form': TransactionForm(request),
            'rform': RequestForm(),
        }
    )


@login_required
def get_chat(request, chat_id):
    try:
        chat = ChatRoom.objects.get(id=chat_id)
        for subscriber in chat.subscribers.all():
            if subscriber != request.user:
                otheruser = subscriber
        messages = chat.messages.all().order_by('timestamp')
    except ObjectDoesNotExist:
        messages = None
        otheruser = None
    if 'floating' in request.GET:
        return render(
            request,
            'messagingsystem/chat_float.html',
            {
                'messages': messages,
                'chat_id': chat.id,
                'chat': chat,
                'floating': True,
            }
        )
    return render(
        request,
        'messagingsystem/chats.html',
        {
            'messages': messages,
            'chat_id': chat.id,
            'floating': True,
            'modals': True,
            'otheruser': otheruser,
            'form': TransactionForm(request),
            'rform': RequestForm(),
        }
    )


@login_required
def create_chat(request, to_user):
    user = User.objects.get(id=to_user)
    label = request.user.username + user.username
    label1 = user.username + request.user.username
    try:
        room1 = ChatRoom.objects.get(name=label)
    except ObjectDoesNotExist:
        room1 = None
    try:
        room2 = ChatRoom.objects.get(name=label1)
    except ObjectDoesNotExist:
        room2 = None
    if room1 or room2:
        if room1:
            chat = room1
        else:
            chat = room2
    else:
        chat, created = ChatRoom.objects.get_or_create(name=label)
        if created:
            chat.subscribers.add(request.user)
            chat.subscribers.add(user)
    messages = chat.messages.all().order_by('timestamp')
    return render(
        request,
        'messagingsystem/chat_float.html',
        {
            'messages': messages,
            'chat_id': chat.id,
            'chat': chat,
            'floating': True
        }
    )


@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chatroom = ChatRoom.objects.get(id=chat_id)
        message = Message(user=request.user)
        message.content = request.POST.get('content')
        message.room = chatroom
        otherusers = []
        for user in chatroom.subscribers.all():
            if user != request.user:
                otherusers.append(user)
        message.to_user = otherusers[0]
        message.save()
        template = loader.get_template(
            'messagingsystem/singlemessage_reciever.html'
        )
        context = {'message': message}
        m = template.render(context)
        message_dict = {
            'chatroom': chatroom.name,
            'message': m,
            'message_id': message.id
        }
        message_json = json.dumps(message_dict)
        for otheruser in otherusers:
            Group('%s-messages' % otheruser.username).send({
                'text': message_json
            })
    return render(
        request,
        'messagingsystem/singlemessage_sender.html',
        {
            'message': message
        }
    )


@login_required
def set_message_status(request):
    if request.method == 'POST':
        message_ids = request.POST.getlist('message_ids')
        for message_id in message_ids:
            message = Message.objects.get(id=message_id)
            message.read = True
            message.save()
        return HttpResponse("OK")
    return HttpResponse("forbidden")
