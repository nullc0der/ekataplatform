from __future__ import division

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from profilesystem.models import UserCompletionRing
from publicusers.models import Connection
# Create your views here.


@login_required
def dashboard_page(request):
    usercomplete, created = \
        UserCompletionRing.objects.get_or_create(user=request.user)
    completed, completed_list, not_completed, not_completed_list, emailadd = \
        usercomplete.calculate_completed()
    connections = Connection.objects.filter(accepted=True)
    connections = connections.filter(
        Q(sender=request.user) | Q(reciever=request.user)
    )
    friends = len(connections.filter(connection_type_main='Friend'))
    families = len(connections.filter(connection_type_main='Family'))
    contacts = len(connections.filter(connection_type_main='Contact'))
    total_conn = friends + families + contacts
    if total_conn:
        friends_percent = (friends / total_conn) * 100
        families_percent = (families / total_conn) * 100
        contacts_percent = (contacts / total_conn) * 100
        no_connection = False
    else:
        friends_percent = 0
        families_percent = 0
        contacts_percent = 0
        no_connection = True
    skipped_list = usercomplete.skipped_list['skipped']
    skipped = len(skipped_list)
    not_verified, not_verified_tasks = usercomplete.calculate_verified()
    total = completed + not_completed + skipped + not_verified
    completed_percent = (completed / total) * 100
    not_completed_percent = (not_completed / total) * 100
    skipped_percent = (skipped / total) * 100
    not_verified_percent = (not_verified / total) * 100
    unread_messages_count = request.user.recieved_messages.filter(
        read=False
    ).count()
    variables = {
        'completed': int(completed_percent),
        'completed_list': completed_list,
        'not_completed': int(not_completed_percent),
        'ncompleted_list': not_completed_list,
        'skipped': int(skipped_percent),
        'skipped_list': skipped_list,
        'not_verified': int(not_verified_percent),
        'nverified_list': not_verified_tasks,
        'emailadd': emailadd,
        'friends': int(friends_percent),
        'families': int(families_percent),
        'contacts': int(contacts_percent),
        'total_conn': total_conn,
        'no_connection': no_connection,
        'unread_messages_count': unread_messages_count
    }
    return render(request, 'dashboard/dashboard.html', context=variables)


@login_required
def skipped_tasks(request):
    if request.is_ajax():
        skipped = request.GET.get("skipped")
        tasks = [
            "website",
            "gender",
            "avatar",
            "phone",
            "address",
            "socialaccount",
            "email",
            "email_verified"
        ]
        usercomplete, created = \
            UserCompletionRing.objects.get_or_create(user=request.user)
        skipped_tasks = usercomplete.skipped_list['skipped']
        if skipped in tasks:
            skipped_tasks.append(skipped)
        usercomplete.skipped_list = {"skipped": skipped_tasks}
        usercomplete.save()
        return HttpResponse("OK")
