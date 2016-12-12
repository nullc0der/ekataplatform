from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from invitationsystem.models import Invitation
from invitationsystem.forms import CheckInvitationForm, GetInvitationForm
from invitationsystem.tasks import send_notification_to_reviewer,\
    task_send_notification_email_to_sms

from autosignup.models import ReferralCode, AccountProvider

# Create your views here.


def index_page(request):
    form = GetInvitationForm()
    if request.method == 'POST':
        form = GetInvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            invitation = Invitation()
            invitation.email = email
            invitation.invitation_id = get_random_string(length=6)
            invitation.save()
            send_notification_to_reviewer.delay(email)
            task_send_notification_email_to_sms.delay(email)
            return render(request, 'invitationsystem/sent.html')
    return render(request, 'invitationsystem/index.html', {'form': form})


def invitation_id_page(request):
    form = CheckInvitationForm()
    accountprovider = AccountProvider.objects.get(name='grantcoin')
    if request.method == 'POST':
        form = CheckInvitationForm(request.POST)
        if form.is_valid():
            request.user.profile.invitation_verified = True
            request.user.profile.save()
            invitation_id = form.cleaned_data.get('invitation_id')
            try:
                invitation = Invitation.objects.get(invitation_id=invitation_id)
                invitation.delete()
            except ObjectDoesNotExist:
                pass
            try:
                referral_code = ReferralCode.objects.get(code=invitation_id)
                request.user.profile.referred_by = referral_code.user
                request.user.profile.save()
            except ObjectDoesNotExist:
                pass
            return redirect(reverse('dashboard:index'))
    return render(
        request,
        'invitationsystem/checkinvitation.html',
        {
            'form': form,
            'accountprovider': accountprovider
        }
    )


@login_required
def referral_code_url(request):
    if 'referral_code' in request.GET:
        referral_code = request.GET.get('referral_code')
        try:
            rcode_obj = ReferralCode.objects.get(code=referral_code)
            request.user.profile.invitation_verified = True
            request.user.profile.referred_by = rcode_obj.user
            request.user.profile.save()
            return redirect(reverse('dashboard:index'))
        except ObjectDoesNotExist:
            return redirect(reverse('invitationsystem:addinvitation'))
    else:
        return redirect(reverse('invitationsystem:addinvitation'))
