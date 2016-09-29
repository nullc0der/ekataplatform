from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    return render(
        request,
        'notification/notification.html',
        {
            'notifications': notifications
        }
    )
