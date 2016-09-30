from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from invitationsystem.models import Invitation
from invitationsystem.forms import CheckInvitationForm
from invitationsystem.tasks import send_notification_to_reviewer

# Create your views here.


def index_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        invitation = Invitation()
        invitation.email = email
        invitation.invitation_id = get_random_string(length=6)
        invitation.save()
        send_notification_to_reviewer.delay(email)
        return HttpResponse("OK")
    return render(request, 'invitationsystem/index.html')


def invitation_id_page(request):
    form = CheckInvitationForm()
    if request.method == 'POST':
        form = CheckInvitationForm(request.POST)
        if form.is_valid():
            request.user.profile.invitation_verified = True
            request.user.profile.save()
            invitation_id = form.cleaned_data.get('invitation_id')
            invitation = Invitation.objects.get(invitation_id=invitation_id)
            invitation.delete()
            return redirect(reverse('dashboard:index'))
    return render(
        request,
        'invitationsystem/checkinvitation.html',
        {
            'form': form
        }
    )
