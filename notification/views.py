import json

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader

# Create your views here.


@login_required
def notifications_view(request):
    notifications = request.user.notifications.filter(
        read=False
    ).order_by('-timestamp')
    template = loader.get_template('notification/notification.html')
    contexts = {'notifications': notifications}
    notification_html = template.render(contexts)
    response_data = {
        'unread': len(notifications),
        'html_s': notification_html
    }
    response = json.dumps(response_data)
    content_type = 'application/json'
    return HttpResponse(response, content_type)


@login_required
def set_notificationread(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = request.user.notifications.get(id=notification_id)
            notification.read = True
            notification.save()
        except ObjectDoesNotExist:
            pass
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()
