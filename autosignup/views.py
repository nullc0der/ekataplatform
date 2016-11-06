from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from autosignup.models import CommunitySignup, EmailVerfication
from autosignup.forms import UserInfoForm, AddressForm, EmailForm, EmailVerficationForm
from autosignup.utils import send_email_verification_code
# Create your views here.


def index_page(request):
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
    return render(
        request,
        'autosignup/index.html',
    )


def step_1_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    uform = UserInfoForm(instance=request.user, prefix='userinfo')
    form = AddressForm(instance=request.user.address)
    if request.method == 'POST':
        uform = UserInfoForm(request.POST, instance=request.user, prefix='userinfo')
        form = AddressForm(request.POST, instance=request.user.address)
        if uform.is_valid() and form.is_valid():
            uform.save()
            form.save()
            community_signup.step_1_done = True
            community_signup.save()
            return HttpResponse(reverse('autosignup:step_2_signup', args=[community_signup.id, ]))
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


def step_2_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if community_signup.step_1_done:
        form = EmailForm(initial={'email': request.user.email})
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                code = get_random_string(length=6)
                send_email_verification_code(form.cleaned_data.get('email'), code)
                community_signup.useremail = form.cleaned_data.get('email')
                community_signup.save()
                emailverfication = EmailVerfication(
                    code=code,
                    user=request.user,
                    community_signup=community_signup
                )
                emailverfication.save()
                return HttpResponse(reverse('autosignup:step_2_verification', args=[community_signup.id, ]))
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
                return HttpResponse(reverse('autosignup:step_3_signup', args=[community_signup.id, ]))
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


def step_3_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    return render(
        request,
        'autosignup/complete_previous_step.html',
        {'community_signup': community_signup}
    )
