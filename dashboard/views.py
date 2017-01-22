from __future__ import division
import datetime
import json
import csv
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from profilesystem.models import UserCompletionRing
from publicusers.models import Connection
from dashboard.models import ActiveMemberCount, NewMemberCount,\
    TotalMemberCount
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
    activemembercounts = ActiveMemberCount.objects.filter(
        date__lte=datetime.datetime.today(),
        date__gt=datetime.datetime.today() - datetime.timedelta(days=30)
    ).order_by('date')
    newmembercounts = NewMemberCount.objects.filter(
        date__lte=datetime.datetime.today(),
        date__gt=datetime.datetime.today() - datetime.timedelta(days=30)
    ).order_by('date')
    totalmembercounts = TotalMemberCount.objects.filter(
        date__lte=datetime.datetime.today(),
        date__gt=datetime.datetime.today() - datetime.timedelta(days=30)
    ).order_by('date')
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
        'unread_messages_count': unread_messages_count,
        'activemembercounts': activemembercounts,
        'newmembercounts': newmembercounts,
        'totalmembercounts': totalmembercounts
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


@login_required
def download_member_stats(request):
    stat_type = request.GET.get('stat')
    filename = '/tmp/%s.csv' % get_random_string()
    download_filename = 'blank'
    f = open(filename, 'w+')
    fieldnames = ['date', 'count']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    if stat_type == 'active_member':
        activemembercounts = ActiveMemberCount.objects.all().order_by('date')
        for activemembercount in activemembercounts:
            row = {}
            row['date'] = "{0}/{1}/{2}".format(
                activemembercount.date.day,
                activemembercount.date.month,
                activemembercount.date.year
            )
            row['count'] = activemembercount.users.count()
            writer.writerow(row)
        download_filename = 'active_member_stats'
    if stat_type == 'new_member':
        newmembercounts = NewMemberCount.objects.all().order_by('date')
        for newmembercount in newmembercounts:
            row = {}
            row['date'] = "{0}/{1}/{2}".format(
                newmembercount.date.day,
                newmembercount.date.month,
                newmembercount.date.year
            )
            row['count'] = newmembercount.count
            writer.writerow(row)
        download_filename = 'new_users_stats'
    if stat_type == 'total_member':
        totalmembercounts = TotalMemberCount.objects.all().order_by('date')
        for totalmembercount in totalmembercounts:
            row = {}
            row['date'] = "{0}/{1}/{2}".format(
                totalmembercount.date.day,
                totalmembercount.date.month,
                totalmembercount.date.year
            )
            row['count'] = totalmembercount.count
            writer.writerow(row)
        download_filename = 'total_member_stats'
    f.close()
    f = open(filename)
    csv_data = f.read()
    f.close()
    os.remove(f.name)
    response = HttpResponse(
        csv_data,
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(
        download_filename
    )
    return response
