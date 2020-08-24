from __future__ import division

import json
from django.http import HttpResponse, HttpResponseServerError
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from publicusers.models import Thumbs, Connection
from usertimeline.models import UserTimeline
from profilesystem.models import UserCompletionRing
from notification.utils import create_notification

# Create your views here.


@login_required
def users_page(request):
    users = User.objects.exclude(
        username='AnonymousUser').exclude(username=request.user.username)
    page_template = 'publicusers/users.html'
    template = 'publicusers/userlist.html'
    filter_changed = False
    original_filters = ['online', 'offline', 'staff', 'member']
    filters_enabled = original_filters
    if 'filters_enabled' in request.session:
        filters_enabled = request.session['filters_enabled']
        if not set(filters_enabled).issuperset(set(original_filters)):
            filter_changed = True
    if 'filters_enabled' in request.GET:
        filters_enabled = request.GET.getlist('filters_enabled')
        if not set(filters_enabled).issuperset(set(original_filters)):
            filter_changed = True
    if filter_changed:
        if 'staff' in filters_enabled and 'member' in filters_enabled:
            users = users
        else:
            if 'staff' in filters_enabled:
                users = users.filter(is_staff=True)
            if 'member' in filters_enabled:
                users = users.filter(is_staff=False)
        if 'online' in filters_enabled and 'offline' in filters_enabled:
            users = users
        else:
            if 'online' in filters_enabled:
                online_users = []
                for u in users:
                    if hasattr(u, 'profile'):
                        if u.profile.online():
                            online_users.append(u)
                users = online_users
            if 'offline' in filters_enabled:
                offline_users = []
                for u in users:
                    if hasattr(u, 'profile'):
                        if not u.profile.online():
                            offline_users.append(u)
                users = offline_users
    if 'q' in request.GET:
        if type(users) == list:
            users_id = [x.id for x in users]
            users = User.objects.filter(id__in=users_id)
        users = users.filter(username__icontains=request.GET.get('q'))
    request.session['filters_enabled'] = filters_enabled
    if request.is_ajax():
        template = page_template
    return render(
        request,
        template,
        {
            'users': users,
            'page_template': page_template,
            'filters_enabled': filters_enabled if filters_enabled else original_filters
        }
    )


@login_required
def user_details_page(request, id):
    user = get_object_or_404(User, id=id)
    usercomplete, created = \
        UserCompletionRing.objects.get_or_create(user=user)
    completed, completed_list, not_completed, not_completed_list, emailadd = \
        usercomplete.calculate_completed()
    skipped_list = usercomplete.skipped_list['skipped']
    skipped = len(skipped_list)
    not_verified, not_verified_tasks = usercomplete.calculate_verified()
    total = completed + not_completed + skipped + not_verified
    completed_percent = (completed / total) * 100
    not_completed_percent = (not_completed / total) * 100
    skipped_percent = (skipped / total) * 100
    not_verified_percent = (not_verified / total) * 100
    thumbs = user.thumbs.all().filter(from_user=request.user)
    connections = Connection.objects.filter(accepted=True)
    connections = connections.filter(
        Q(sender=user) | Q(reciever=user)
    )
    friends = len(connections.filter(connection_type_main='Friend'))
    families = len(connections.filter(connection_type_main='Family'))
    contacts = len(connections.filter(connection_type_main='Contact'))
    conn_sent = Connection.objects.filter(sender=request.user, reciever=user)
    if conn_sent:
        conn_id = conn_sent[0].id
        if conn_sent[0].accepted:
            conn_type = conn_sent[0].connection_type_main
            disconnect = True
            cancel = False
            reject = False
        else:
            cancel = True
            disconnect = False
            reject = False
            conn_type = None
    else:
        disconnect = False
        cancel = False
        reject = False
        conn_id = None
        conn_type = None
    conn_recieved = Connection.objects.filter(
        sender=user,
        reciever=request.user
    )
    if conn_recieved:
        conn_id = conn_recieved[0].id
        if conn_recieved[0].accepted:
            conn_type = conn_recieved[0].connection_type_main
            disconnect = True
            cancel = False
            reject = False
        else:
            reject = True
            cancel = False
            disconnect = False
            conn_type = None
    if thumbs:
        for thumb in thumbs:
            thumb_id = thumb.id
            if thumb.is_public:
                public = True
            else:
                public = False
        thumb_uped = True
    else:
        thumb_id = None
        thumb_uped = False
        public = True
    if 'thumbs' in request.GET:
        thumb, created = Thumbs.objects.update_or_create(
            user=user,
            from_user=request.user
        )
        if created:
            sendertimeline = UserTimeline(
                user=request.user,
                timeline_type=4,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id
            )
            sendertimeline.save()
            recievertimeline = UserTimeline(
                user=user,
                timeline_type=4,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id
            )
            recievertimeline.save()
            create_notification(
                user=user,
                ntype=4,
                sender=request.user.username,
                sender_id=request.user.id,
                timeline_id=recievertimeline.id
            )
            return HttpResponse(_("Success"))
        else:
            return HttpResponse(_("You already thumb uped this user"))
    if 'public' in request.GET:
        public = request.GET.get('public')
        if public == 'true':
            thumb, created = Thumbs.objects.update_or_create(
                user=user,
                from_user=request.user
            )
            thumb.is_public = True
            thumb.save()
            return HttpResponse('OK')
        else:
            thumb, created = Thumbs.objects.update_or_create(
                user=user,
                from_user=request.user,
            )
            thumb.is_public = False
            thumb.save()
            return HttpResponse('OK')
    if request.method == "POST":
        thumb_id = request.POST.get('unverify', None)
        if thumb_id:
            thumb = Thumbs.objects.get(id=thumb_id)
            thumb.delete()
            sendertimeline = UserTimeline(
                user=request.user,
                timeline_type=5,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id
            )
            sendertimeline.save()
            recievertimeline = UserTimeline(
                user=user,
                timeline_type=5,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id
            )
            recievertimeline.save()
            create_notification(
                user=user,
                ntype=5,
                sender=request.user.username,
                sender_id=request.user.id,
                timeline_id=recievertimeline.id
            )
            return render(
                request,
                'publicusers/userdetails.html',
                {
                    'user': user,
                    'public': public,
                }
            )
    if request.is_ajax():
        return render(
            request,
            'publicusers/user.html',
            {
                'user': user,
                'completed': int(completed_percent),
                'not_completed': int(not_completed_percent),
                'skipped': int(skipped_percent),
                'not_verified': int(not_verified_percent),
                'ajaxr': True,
                'friends': friends,
                'families': families,
                'contacts': contacts
            }
        )
    return render(
        request,
        'publicusers/userdetails.html',
        {
            'user': user,
            'public': public,
            'thumb_uped': thumb_uped,
            'thumb_id': thumb_id,
            'completed': int(completed_percent),
            'not_completed': int(not_completed_percent),
            'skipped': int(skipped_percent),
            'not_verified': int(not_verified_percent),
            'friends': friends,
            'families': families,
            'contacts': contacts,
            'disconnect': disconnect,
            'reject': reject,
            'cancel': cancel,
            'conn_id': conn_id,
            'conn_type': conn_type
        }
    )


@login_required
def send_sub_connection(request):
    if 'mainconn' in request.GET and request.is_ajax():
        mainconn = request.GET.get('mainconn')
        if mainconn == 'Friend':
            subconn = {
                'main': unicode(_('Friend type')),
                'sub': [unicode(_('Best')), unicode(_('Friend')), unicode(_('Soulmate')), unicode(_('Acquaintance'))]
            }
        if mainconn == 'Family':
            subconn = {
                'main': unicode(_('Family type')),
                'sub': [
                    unicode(_('Father')),
                    unicode(_('Son')),
                    unicode(_('Husband')),
                    unicode(_('Brother')),
                    unicode(_('Grandfather')),
                    unicode(_('Grandson')),
                    unicode(_('Uncle')),
                    unicode(_('Nephew')),
                    unicode(_('Cousin')),
                    unicode(_('Mother')),
                    unicode(_('Daughter')),
                    unicode(_('Wife')),
                    unicode(_('Sister')),
                    unicode(_('Grandmother')),
                    unicode(_('Granddaughter')),
                    unicode(_('Aunt')),
                    unicode(_('Niece')),
                    unicode(_('Cousin')),
                    unicode(_('Parent')),
                    unicode(_('Child')),
                    unicode(_('Spouse')),
                    unicode(_('Sibling')),
                    unicode(_('Grandparent')),
                    unicode(_('Grandchild'))
                ]
            }
        if mainconn == 'Contact':
            subconn = {
                'main': unicode(_('Contact type')),
                'sub': [unicode(_('Personal')), unicode(_('Business'))]
            }
    data = json.dumps(subconn)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def request_connection(request, user):
    if request.method == 'POST':
        reciever = get_object_or_404(User, id=user)
        conn_main = request.POST.get('connmain')
        conn_sub = request.POST.get('connsub')
        conn_exist = Connection.objects.filter(sender=reciever, reciever=request.user)
        if len(conn_exist):
            return HttpResponseServerError(_("connection already sent by ") + reciever.username)
        conn = Connection(
            sender=request.user,
            reciever=reciever,
            connection_type_main=conn_main,
            connection_type_sub=conn_sub
        )
        conn.save()
        sendertimeline = UserTimeline(
            user=request.user,
            timeline_type=6,
            sender=request.user.username,
            sender_id=request.user.id,
            reciever=reciever.username,
            reciever_id=reciever.id,
            conn_main=conn_main,
            conn_sub=conn_sub,
            conn_id=conn.id
        )
        recievertimeline = UserTimeline(
            user=reciever,
            timeline_type=6,
            sender=request.user.username,
            sender_id=request.user.id,
            reciever=reciever.username,
            reciever_id=reciever.id,
            conn_main=conn_main,
            conn_sub=conn_sub,
            conn_id=conn.id
        )
        sendertimeline.save()
        recievertimeline.save()
        create_notification(
            user=reciever,
            ntype=6,
            sender=request.user.username,
            sender_id=request.user.id,
            timeline_id=recievertimeline.id
        )
    return HttpResponse(_("A request is sent to ") + reciever.username)


@login_required
def accept_connection(request, conn_id):
    if request.method == 'POST':
        connection = get_object_or_404(Connection, id=conn_id)
        connection.accepted = True
        connection.save()
        timelines = UserTimeline.objects.filter(conn_id=conn_id)
        for timeline in timelines:
            timeline.accepted = True
            timeline.save()
        create_notification(
            user=connection.sender,
            ntype=8,
            sender=request.user.username,
            sender_id=request.user.id,
        )
    return HttpResponse(_("Connection accepted"))


@login_required
def cancel_reject_connection(request, conn_id):
    if request.method == 'POST':
        tipe = request.POST.get('type')
        connection = get_object_or_404(Connection, id=conn_id)
        if tipe == 'cancel':
            create_notification(
                user=connection.reciever,
                ntype=7,
                sender=request.user.username,
                sender_id=request.user.id,
            )
        if tipe == 'reject':
            create_notification(
                user=connection.sender,
                ntype=9,
                sender=request.user.username,
                sender_id=request.user.id,
            )
        if tipe == 'disconnect':
            if connection.sender == request.user:
                create_notification(
                    user=connection.reciever,
                    ntype=10,
                    sender=request.user.username,
                    sender_id=request.user.id,
                )
            else:
                create_notification(
                    user=connection.sender,
                    ntype=10,
                    sender=request.user.username,
                    sender_id=request.user.id,
                )
        connection.delete()
        timelines = UserTimeline.objects.filter(conn_id=conn_id)
        for timeline in timelines:
            timeline.delete()
    if tipe == 'cancel':
        return HttpResponse(_("Canceled connection request"))
    elif tipe == 'reject':
        return HttpResponse(_("Rejected connection"))
    elif tipe == 'disconnect':
        return HttpResponse(_('Disconneted'))
    else:
        return HttpResponse(_("Success!!"))


@login_required
def show_connection(request):
    connections = Connection.objects.filter(accepted=True)
    connections = connections.filter(
        Q(sender=request.user) | Q(reciever=request.user)
    )
    valid_conn = ['Friend', 'Family', 'Contact']
    conn_type = request.GET.get('conn_type')
    if conn_type in valid_conn:
        users = []
        title = _(conn_type)
        connections = connections.filter(connection_type_main=conn_type)
        for connection in connections:
            users.append(connection.sender)
            users.append(connection.reciever)
        if 'username' in request.GET:
            username = request.GET.get('username')
            if username:
                users = []
                connections = connections.filter(
                    Q(sender__username__istartswith=username) |
                    Q(reciever__username__istartswith=username)
                )
                for connection in connections:
                    users.append(connection.sender)
                    users.append(connection.reciever)
        paginator = Paginator(users, 10)  # group the users by 10
        page = request.GET.get('page')  # get page no
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integet, deliver first page
            users = paginator.page(1)
    if 'username' in request.GET:
        return render(
            request,
            'publicusers/connusers.html',
            {
                'users': users,
                'title': title
            }
        )
    else:
        return render(
            request,
            'publicusers/connections.html',
            {
                'users': users,
                'title': title
            }
        )


@login_required
def get_onlinestate(request, id):
    user = User.objects.get(id=id)
    is_online = user.profile.online()
    last_seen = user.profile.last_seen()
    state = {
        'last_seen': last_seen,
        'is_online': is_online
    }
    data = json.dumps(state, default=date_handler)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def get_onlineusers(request):
    users_status = {}
    users = User.objects.all()
    for user in users:
        if hasattr(user, 'profile') and not user == request.user:
            if user.profile.online():
                users_status[user.id] = "online"
            else:
                users_status[user.id] = user.profile.last_seen()
    data = json.dumps(users_status, default=date_handler)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def get_onlineusers_react(request):
    online_users = []
    users = User.objects.all()
    for user in users:
        if hasattr(user, 'profile'):
            if user.profile.online():
                online_users.append(user.username)
    data = json.dumps(online_users)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


@login_required
def get_missing_users(request):
    userslist = request.GET.getlist('users')
    users = []
    for id in userslist:
        try:
            user = User.objects.get(id=id)
            users.append(user)
        except ObjectDoesNotExist:
            pass
    return render(
        request,
        'publicusers/missing_users.html',
        {
            'users': users
        }
    )
