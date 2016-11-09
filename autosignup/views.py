import json
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from autosignup.models import CommunitySignup, EmailVerfication,\
    PhoneVerification
from autosignup.forms import UserInfoForm, AddressForm, EmailForm,\
    EmailVerficationForm, PhoneForm, PhoneVerificationForm, AdditionalStepForm
from autosignup.tasks import task_send_email_verfication_code,\
    task_send_phone_verfication_code
from autosignup.utils import collect_twilio_data
from profilesystem.models import UserAddress, UserPhone
# Create your views here.


@login_required
def index_page(request):
    return render(
        request,
        'autosignup/index.html',
    )


@login_required
def check_step(request):
    if 'community_name' in request.GET:
        community_name = request.GET.get('community_name')
        community_signup, created = CommunitySignup.objects.get_or_create(
            user=request.user,
            community=community_name
        )
        if not community_signup.step_1_done:
            return HttpResponse(reverse(
                    'autosignup:step_1_signup',
                    args=[community_signup.id, ]
                ))
        if not community_signup.step_2_done:
            return HttpResponse(reverse(
                    'autosignup:step_2_signup',
                    args=[community_signup.id, ]
                ))
        if not community_signup.step_3_done:
            return HttpResponse(reverse(
                    'autosignup:step_3_signup',
                    args=[community_signup.id, ]
                ))
        if community_signup.failed_auto_signup and not community_signup.additional_step_done:
            return HttpResponse(reverse(
                    'autosignup:additional_step',
                    args=[community_signup.id, ]
                ))
    return HttpResponse(reverse(
            'autosignup:thankyou'
        ))


@login_required
def step_1_signup(request, id):
    try:
        address = request.user.address
    except ObjectDoesNotExist:
        address = UserAddress(user=request.user)
        address.save()
    community_signup = CommunitySignup.objects.get(id=id)
    uform = UserInfoForm(instance=request.user, prefix='userinfo')
    form = AddressForm(instance=address)
    if request.method == 'POST':
        uform = UserInfoForm(request.POST, instance=request.user, prefix='userinfo')
        form = AddressForm(request.POST, instance=address)
        if uform.is_valid() and form.is_valid():
            uform.save()
            form.save()
            useraddress_in_db = ''
            for k, v in uform.cleaned_data.iteritems():
                useraddress_in_db = useraddress_in_db + '%s: %s ; \n' % (k, v)
            for k, v in form.cleaned_data.iteritems():
                useraddress_in_db = useraddress_in_db + '%s: %s ; \n' % (k, v)
            community_signup.useraddress_in_db = useraddress_in_db
            community_signup.step_1_done = True
            community_signup.save()
            data = {
                'action': 'next',
                'url': reverse('autosignup:step_2_signup', args=[community_signup.id, ])
            }
            json_data = json.dumps(data)
            content_type = 'application/json'
            return HttpResponse(json_data, content_type)
        else:
            return render(
                request,
                'autosignup/step_1_form.html',
                {'form': form, 'uform': uform, 'community_signup': community_signup},
                status=500
            )
    return render(
        request,
        'autosignup/step_1_form.html',
        {'form': form, 'uform': uform, 'community_signup': community_signup}
    )


@login_required
def step_2_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if community_signup.step_1_done:
        form = EmailForm(initial={'email': request.user.email})
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                code = get_random_string(length=6)
                task_send_email_verfication_code.delay(
                    form.cleaned_data.get('email'),
                    code
                )
                community_signup.useremail = form.cleaned_data.get('email')
                community_signup.save()
                emailverfication = EmailVerfication(
                    code=code,
                    user=request.user,
                    community_signup=community_signup
                )
                emailverfication.save()
                data = {
                    'action': 'next',
                    'url': reverse('autosignup:step_2_verification', args=[community_signup.id, ])
                }
                json_data = json.dumps(data)
                content_type = 'application/json'
                return HttpResponse(json_data, content_type)
            else:
                return render(
                    request,
                    'autosignup/step_2_form.html',
                    {'form': form, 'community_signup': community_signup},
                    status=500
                )
        return render(
            request,
            'autosignup/step_2_form.html',
            {'form': form, 'community_signup': community_signup}
        )
    else:
        return render(
            request,
            'autosignup/complete_previous_step.html',
            {'community_signup': community_signup}
        )


@login_required
def verify_email_code(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if community_signup.step_1_done:
        form = EmailVerficationForm(community_signup, request)
        if request.method == 'POST':
            form = EmailVerficationForm(community_signup, request, request.POST)
            if form.is_valid():
                community_signup.step_2_done = True
                community_signup.save()
                request.user.email = community_signup.useremail
                request.user.save()
                emailverfication = EmailVerfication.objects.get(
                    user=request.user,
                    community_signup=community_signup,
                    code=form.cleaned_data.get('verification_code')
                )
                emailverfication.delete()
                data = {
                    'action': 'next',
                    'url': reverse('autosignup:step_3_signup', args=[community_signup.id, ])
                }
                json_data = json.dumps(data)
                content_type = 'application/json'
                return HttpResponse(json_data, content_type)
            else:
                return render(
                    request,
                    'autosignup/step_2_verification.html',
                    {'form': form, 'community_signup': community_signup},
                    status=500
                )
        return render(
            request,
            'autosignup/step_2_verification.html',
            {
                'form': form,
                'community_signup': community_signup
            }
        )
    else:
        return render(
            request,
            'autosignup/complete_previous_step.html',
            {'community_signup': community_signup}
        )


@login_required
def step_3_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if community_signup.step_1_done and community_signup.step_2_done:
        form = PhoneForm()
        if request.method == 'POST':
            form = PhoneForm(request.POST)
            if form.is_valid():
                code = get_random_string(length=6)
                phone = form.cleaned_data.get('country') + form.cleaned_data.get('phone_no')
                task_send_phone_verfication_code.delay(phone, code)
                community_signup.userphone = phone
                community_signup.save()
                phoneverfication = PhoneVerification(
                    code=code,
                    user=request.user,
                    community_signup=community_signup
                )
                phoneverfication.save()
                data = {
                    'action': 'next',
                    'url': reverse('autosignup:step_3_verification', args=[community_signup.id, ])
                }
                json_data = json.dumps(data)
                content_type = 'application/json'
                return HttpResponse(json_data, content_type)
            else:
                return render(
                    request,
                    'autosignup/step_3_form.html',
                    {'form': form, 'community_signup': community_signup},
                    status=500
                )
        return render(
            request,
            'autosignup/step_3_form.html',
            {'form': form, 'community_signup': community_signup}
        )
    else:
        return render(
            request,
            'autosignup/complete_previous_step.html',
            {'community_signup': community_signup}
            )


@login_required
def verify_phone_code(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if community_signup.step_1_done and community_signup.step_2_done:
        form = PhoneVerificationForm(community_signup, request)
        if request.method == 'POST':
            form = PhoneVerificationForm(community_signup, request, request.POST)
            if form.is_valid():
                phoneverfication = PhoneVerification.objects.get(
                    user=request.user,
                    community_signup=community_signup,
                    code=form.cleaned_data.get('verification_code')
                )
                phoneverfication.delete()
                twilio_data = collect_twilio_data(community_signup.userphone)
                if twilio_data:
                    community_signup.useraddress_from_twilio = twilio_data
                    community_signup.step_3_done = True
                    community_signup.failed_auto_signup = True
                    community_signup.save()
                else:
                    community_signup.step_3_done = True
                    community_signup.failed_auto_signup = True
                    community_signup.save()
                data = {
                    'action': 'next',
                    'url': reverse('autosignup:additional_step', args=[community_signup.id, ])
                }
                json_data = json.dumps(data)
                content_type = 'application/json'
                return HttpResponse(json_data, content_type)
            else:
                return render(
                    request,
                    'autosignup/step_3_verification.html',
                    {'form': form, 'community_signup': community_signup},
                    status=500
                )
        return render(
            request,
            'autosignup/step_3_verification.html',
            {
                'form': form,
                'community_signup': community_signup
            }
        )
    else:
        return render(
            request,
            'autosignup/complete_previous_step.html',
            {'community_signup': community_signup}
        )


def additional_step(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if request.method == 'POST':
        form = AdditionalStepForm(request.POST, request.FILES)
        if form.is_valid():
            community_signup.userimage = form.cleaned_data.get('userimage')
            community_signup.additional_step_done = True
            community_signup.save()
            data = {
                'action': 'thankyou',
                'url': reverse('autosignup:thankyou')
            }
            json_data = json.dumps(data)
            content_type = 'application/json'
            return HttpResponse(json_data, content_type)
        else:
            return render(
                request,
                'autosignup/additional_step.html',
                {
                    'community_signup': community_signup,
                    'form': form
                },
                status=500
            )
    return render(
        request,
        'autosignup/additional_step.html',
        {
            'community_signup': community_signup,
            'form': AdditionalStepForm()
        }
    )
