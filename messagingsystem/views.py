import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from channels import Group

from messagingsystem.models import ChatRoom, Message
from dashboard.models import TotalMessageCount

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
        if chats[0].subscribers.all().count() > 1:
            for subscriber in chats[0].subscribers.all():
                if subscriber != request.user:
                    otheruser = subscriber
        else:
            for unsubscriber in chats[0].unsubscribers.all():
                if unsubscriber != request.user:
                    otheruser = unsubscriber
    else:
        messages = None
        chat_id = None
        otheruser = None
    if 'navbar' in request.GET:
        has_unread = 0
        unread_messages = request.user.recieved_messages.filter(
            read=False
        )
        for unread_message in unread_messages:
            if request.user in unread_message.room.subscribers.all():
                has_unread += 1
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
        }
    )


@login_required
def get_chat(request, chat_id):
    messages = None
    otheruser = None
    try:
        chat = ChatRoom.objects.get(id=chat_id)
        if chat.subscribers.all() > 1:
            for subscriber in chat.subscribers.all():
                if subscriber != request.user:
                    otheruser = subscriber
        else:
            for unsubscriber in chat.unsubscribers.all():
                if unsubscriber != request.user:
                    otheruser = unsubscriber
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
        }
    )


@login_required
def create_chat(request, to_user):
    from_react = request.GET.get('react', False)
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
        if request.user in chat.unsubscribers.all():
            chat.unsubscribers.remove(request.user)
            chat.subscribers.add(request.user)
    else:
        chat, created = ChatRoom.objects.get_or_create(name=label)
        if created:
            chat.subscribers.add(request.user)
            chat.subscribers.add(user)
    messages = chat.messages.all().order_by('timestamp')
    if from_react:
        return JsonResponse({'id': chat.id})
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
        if otherusers:
            message.to_user = otherusers[0]
        else:
            for user in chatroom.unsubscribers.all():
                if user != request.user:
                    message.to_user = user
        message.save()
        totalmessagecount, created = TotalMessageCount.objects.get_or_create(
            date=now().date()
        )
        totalmessagecount.count += 1
        totalmessagecount.save()
        if otherusers:
            template = loader.get_template(
                'messagingsystem/singlemessage_reciever.html'
            )
            context = {'message': message}
            m = template.render(context)
            message_dict = {
                'chatroom': chatroom.name,
                'message': m,
                'message_id': message.id,
                'add_message': True
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


@require_POST
@login_required
def delete_message(request):
    try:
        message = Message.objects.get(id=request.POST.get('id'))
        if message.user == request.user:
            chatroom = message.room
            otherusers = []
            for user in chatroom.subscribers.all():
                if user != request.user:
                    otherusers.append(user)
            if otherusers:
                message_dict = {
                    'chatroom': chatroom.name,
                    'message_id': message.id,
                    'add_message': False
                }
                message_json = json.dumps(message_dict)
                for otheruser in otherusers:
                    Group('%s-messages' % otheruser.username).send({
                        'text': message_json
                    })
                message.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        return HttpResponse(status=500)


@require_POST
@login_required
def delete_chatroom(request):
    try:
        room = ChatRoom.objects.get(id=request.POST.get('id'))
        if request.user in room.subscribers.all():
            room.subscribers.remove(request.user)
            room.unsubscribers.add(request.user)
            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        return HttpResponse(status=500)


@require_POST
@login_required
def delete_messages(request):
    messages = Message.objects.filter(id__in=request.POST.getlist('ids'))
    otherusers = set()
    data = []
    message_ids = []
    for message in messages:
        if message.user == request.user:
            chatroom = message.room
            for user in chatroom.subscribers.all():
                if user != request.user:
                    otherusers.add(user)
            message_dict = {
                'chatroom': chatroom.id,
                'message_id': message.id,
                'add_message': False
            }
            data.append(message_dict)
            message_ids.append(message.id)
            message.delete()
    message_json = json.dumps(data)
    if otherusers:
        for otheruser in otherusers:
            Group('%s-messages' % otheruser.username).send({
                'text': message_json
            })
    return HttpResponse(
        content=json.dumps(message_ids),
        status=200, content_type='application/json')


@require_POST
@login_required
def set_typing_status(request):
    try:
        chatroom = ChatRoom.objects.get(id=request.POST.get('chatroom'))
        if request.user in chatroom.subscribers.all():
            otherusers = []
            for user in chatroom.subscribers.all():
                if request.user != user:
                    otherusers.append(user)
            for otheruser in otherusers:
                message_dict = {
                    'chatroom': chatroom.id,
                    'typing': True
                }
                Group('%s-messages' % otheruser.username).send({
                    'text': json.dumps(message_dict)
                })
            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
