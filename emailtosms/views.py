from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from emailtosms.models import Carrier, Verifier
from emailtosms.forms import ConfirmationForm, VerificationForm
from emailtosms.utils import send_carrier_code_email

# Create your views here.


@login_required
def emailtosms_page(request):
    form = ConfirmationForm()
    vform = VerificationForm(request)
    return render(
        request,
        'emailtosms/index.html',
        {
            'form': form,
            'vform': vform
        }
    )


@login_required
def add_verifier(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            carrier = form.cleaned_data.get('carrier')
            phone_number = form.cleaned_data.get('phone_number')
            verifier, created = Verifier.objects.get_or_create(
                carrier=carrier,
                user=request.user
            )
            verifier.save()
            send_carrier_code_email(
                carrier.emailaddress,
                phone_number,
                verifier.code
            )
            return HttpResponse("ok")
        else:
            return render(
                request,
                'emailtosms/verifierform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerificationForm(request, request.POST)
        if form.is_valid():
            verifier = Verifier.objects.filter(
                user=request.user,
                code=form.cleaned_data.get('code')
            )
            if verifier:
                carrier = verifier[0].carrier
                carrier.verified = True
                carrier.verified_times += 1
                carrier.save()
            for v in verifier:
                v.delete()
            return HttpResponse('OK')
        else:
            return render(
                request,
                'emailtosms/verificationform.html',
                {
                    'vform': form
                },
                status=500
            )
    else:
        return HttpResponseForbidden()
