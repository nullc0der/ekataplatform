from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from usertimeline.models import UserTimeline, TimelineSetting

# Create your views here.


@login_required
def timeline_page(request):
    timelinesetting, created = \
        TimelineSetting.objects.get_or_create(user=request.user)
    timelines = UserTimeline.objects.filter(
        user=request.user
    ).order_by('-timestamp')
    enabled_filters = timelinesetting.enabled_filters['enabled']
    click_counts = timelinesetting.click_counts
    if enabled_filters:
        q_obj = Q()
        for enabled_filter in enabled_filters:
            q_obj |= Q(timeline_type=enabled_filter)
        timelines = timelines.filter(q_obj)
    else:
        timelines = []
    return render(
        request,
        'timelines/index.html',
        {
            'timelines': timelines,
            'enabled_filters': enabled_filters,
            'click_counts': click_counts
        }
    )


@login_required
def set_timelinestate(request):
    timelinesetting, created = \
        TimelineSetting.objects.get_or_create(user=request.user)
    click_counts = timelinesetting.click_counts
    if 'count' in request.GET:
        count = request.GET.get('count')
        click_counts[count] += 1
        timelinesetting.save()
    if 'filter' in request.GET:
        fils = request.GET.getlist('filter')
        e_list = []
        for fil in fils:
            if fil:
                e_list.append(fil)
        enabled = {'enabled': e_list}
        timelinesetting.enabled_filters = enabled
        timelinesetting.save()
    return HttpResponse("OK")


def search_timeline(request):
    timelines = UserTimeline.objects.filter(
        user=request.user
    ).order_by('-timestamp')
    username = request.GET.get('username')
    filters = request.GET.getlist('filter')
    q_obj = Q()
    if len(filters) >= 1 and filters[0]:
        for fil in filters:
            if fil:
                q_obj |= Q(timeline_type=fil)
        timelines = timelines.filter(q_obj)
    else:
        timelines = []
    if username:
        timelines = timelines.filter(
            Q(sender__istartswith=username) | Q(reciever__istartswith=username)
        )
    return render(
        request,
        'timelines/timeline.html',
        {
            'timelines': timelines,
        }
    )
