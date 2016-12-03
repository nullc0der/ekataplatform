import os
import json
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.timezone import now
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from allauth.account.models import EmailAddress

from autosignup.models import CommunitySignup, EmailVerfication,\
    PhoneVerification, AccountProvider, GlobalPhone, GlobalEmail,\
    ApprovedMailTemplate, AccountProviderCSV
from autosignup.forms import UserInfoForm, AddressForm, EmailForm,\
    EmailVerficationForm, PhoneForm, PhoneVerificationForm,\
    AdditionalStepForm, AccountAddContactForm, CommunitySignupForm
from autosignup.tasks import task_send_email_verfication_code,\
    task_send_phone_verfication_code, task_send_approval_mail,\
    task_add_member_from_csv
from autosignup.utils import collect_twilio_data, AddressCompareUtil,\
    send_csv_member_invitation_email
from profilesystem.models import UserAddress, UserPhone
from hashtag.views import get_client_ip
from invitationsystem.models import Invitation
from invitationsystem.tasks import send_invitation
# Create your views here.


def get_selected_template_path():
    accountprovider = AccountProvider.objects.get(name='grantcoin')
    mailtemplates = accountprovider.mailtemplate.filter(selected=True)
    if mailtemplates:
        return mailtemplates[0].template.path
    return


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
        accountprovider = AccountProvider.objects.get(name=community_name)
        if accountprovider.signup_is_open:
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
            if community_signup.additional_step_done:
                return HttpResponse(reverse(
                        'autosignup:thankyou'
                    ))
        else:
            return HttpResponse(reverse(
                'autosignup:signupclosed'
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
            g = GeoIP2()
            try:
                c = g.city(get_client_ip(request))
            except:
                c = None
            useraddress_from_geoip = ''
            if c:
                for k, v in c.iteritems():
                    useraddress_from_geoip = useraddress_from_geoip + '%s: %s ; \n' % (k, v)
            community_signup.useraddress_from_geoip = useraddress_from_geoip
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
        if request.user.emailaddress_set.all():
            for emailaddress in request.user.emailaddress_set.all():
                if emailaddress.primary and not emailaddress.verified:
                    email = emailaddress.email
                else:
                    email = None
            form = EmailForm(initial={'email': email})
        else:
            form = EmailForm()
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                code = get_random_string(length=6, allowed_chars='abcdefghjkmnopqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ123456789')
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
                try:
                    emailaddress, created = EmailAddress.objects.get_or_create(
                        user=request.user,
                        email=community_signup.useremail,
                    )
                    emailaddress.verified = True
                    emailaddress.save()
                except:
                    pass
                emailverfication = EmailVerfication.objects.get(
                    user=request.user,
                    community_signup=community_signup,
                    code=form.cleaned_data.get('verification_code')
                )
                try:
                    globalemail = GlobalEmail.objects.get(
                        email=emailverfication.community_signup.useremail
                    )
                    globalemail.signup.add(community_signup)
                except ObjectDoesNotExist:
                    globalemail, created = GlobalEmail.objects.get_or_create(
                        email=emailverfication.community_signup.useremail
                    )
                    globalemail.signup.add(community_signup)
                emailverfication.delete()
                community_signup.save()
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
        form = PhoneForm(request)
        if request.method == 'POST':
            form = PhoneForm(request, request.POST)
            if form.is_valid():
                code = get_random_string(length=6, allowed_chars='0123456789')
                phone = form.cleaned_data.get('country') + form.cleaned_data.get('phone_no')
                if cache.get('%s_phoneretry' % request.user.username):
                    phoneretry = cache.get('%s_phoneretry' % request.user.username)
                    if phone == phoneretry['phone']:
                        phoneretry['retry'] += 1
                        cache.set(
                            '%s_phoneretry' % request.user.username,
                            phoneretry,
                            2 * 60 * 60
                        )
                    else:
                        phoneretry = {
                            'phone': phone,
                            'retry': 0,
                            'first_attempt_time': now()
                        }
                        cache.set(
                            '%s_phoneretry' % request.user.username,
                            phoneretry,
                            2 * 60 * 60
                        )
                else:
                    phoneretry = {
                        'phone': phone,
                        'retry': 0,
                        'first_attempt_time': now()
                    }
                    cache.set(
                        '%s_phoneretry' % request.user.username,
                        phoneretry,
                        2 * 60 * 60
                    )
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
                try:
                    globalphone = GlobalPhone.objects.get(
                        phone=phoneverfication.community_signup.userphone
                    )
                    globalphone.signup.add(community_signup)
                except ObjectDoesNotExist:
                    globalphone, created = GlobalPhone.objects.get_or_create(
                        phone=phoneverfication.community_signup.userphone
                    )
                    globalphone.signup.add(community_signup)
                phoneverfication.delete()
                twilio_data = collect_twilio_data(community_signup.userphone)
                if twilio_data:
                    community_signup.useraddress_from_twilio = twilio_data
                    community_signup.step_3_done = True
                    addresscompareutil = AddressCompareUtil(
                        community_signup.useraddress_in_db.split(';'),
                        twilio_data
                    )
                    distance = addresscompareutil.calculate_distance()
                    if distance:
                        community_signup.distance_db_vs_twilio = distance[0]
                        accountprovider, created = AccountProvider.objects.get_or_create(name='grantcoin')
                        if accountprovider.allowed_distance < distance[1] * 0.000621371:
                            community_signup.signup_status = 'approved'
                            community_signup.sent_to_community_staff = True
                            community_signup.verified_date = now()
                            community_signup.save()
                            template_path = get_selected_template_path()
                            task_send_approval_mail.delay(community_signup, template_path)
                        else:
                            community_signup.failed_auto_signup = True
                            community_signup.auto_signup_fail_reason = 'Distance not within allowed range'
                            community_signup.sent_to_community_staff = True
                            community_signup.save()
                    else:
                        community_signup.failed_auto_signup = True
                        community_signup.auto_signup_fail_reason = 'No distance data'
                        community_signup.sent_to_community_staff = True
                        community_signup.save()
                else:
                    community_signup.step_3_done = True
                    community_signup.failed_auto_signup = True
                    community_signup.auto_signup_fail_reason = 'No data from twilio'
                    community_signup.sent_to_community_staff = True
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


@login_required
def step_3_no_code(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    try:
        globalphone = GlobalPhone.objects.get(
            phone=community_signup.userphone
        )
        globalphone.signup.add(community_signup)
    except ObjectDoesNotExist:
        globalphone, created = GlobalPhone.objects.get_or_create(
            phone=community_signup.userphone
        )
        globalphone.signup.add(community_signup)
    community_signup.not_verifiable_number = True
    community_signup.step_3_done = True
    community_signup.failed_auto_signup = True
    community_signup.auto_signup_fail_reason =\
        "User did'nt get verification code"
    community_signup.sent_to_community_staff = True
    community_signup.save()
    data = {
        'action': 'next',
        'url': reverse(
            'autosignup:additional_step',
            args=[community_signup.id, ]
        )
    }
    json_data = json.dumps(data)
    content_type = 'application/json'
    return HttpResponse(json_data, content_type)


@login_required
def additional_step(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    if request.method == 'POST':
        form = AdditionalStepForm(request.POST, request.FILES)
        if form.is_valid():
            community_signup.userimage = form.cleaned_data.get('userimage')
            community_signup.additional_step_done = True
            community_signup.data_collect_done = True
            community_signup.sent_to_community_staff = True
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


@login_required
def signups_page(request):
    signups = CommunitySignup.objects.filter(
        sent_to_community_staff=True
    ).filter(status='pending')
    email_used_for_signups = []
    phone_used_for_signups = []
    if request.user.profile.grantcoin_staff or request.user.is_superuser:
        if 'signup_id' in request.GET:
            signup = CommunitySignup.objects.get(
                id=request.GET.get('signup_id')
            )
            if signup.globalphone.all():
                globalphones = GlobalPhone.objects.filter(phone=signup.userphone)
                for globalphone in globalphones:
                    if len(globalphone.signup.all()) >= 2:
                        for sign in globalphone.signup.all():
                            phone_used_for_signups.append(sign)
            if signup.globalemail.all():
                globalemails = GlobalEmail.objects.filter(email=signup.useremail)
                for globalemail in globalemails:
                    if len(globalemail.signup.all()) >= 2:
                        for sign in globalemail.signup.all():
                            email_used_for_signups.append(sign)
            return render(
                request,
                'autosignup/signupinfo.html',
                {
                    'signup': signup,
                    'globalemails': email_used_for_signups if email_used_for_signups else None,
                    'globalphones': phone_used_for_signups if email_used_for_signups else None
                }
            )
        if signup.globalphone.all():
            globalphones = GlobalPhone.objects.filter(phone=signup.userphone)
            for globalphone in globalphones:
                if len(globalphone.signup.all()) >= 2:
                    for sign in globalphone.signup.all():
                        phone_used_for_signups.append(sign)
        if signup.globalemail.all():
            globalemails = GlobalEmail.objects.filter(email=signup.useremail)
            for globalemail in globalemails:
                if len(globalemail.signup.all()) >= 2:
                    for sign in globalemail.signup.all():
                        email_used_for_signups.append(sign)
        return render(
            request,
            'autosignup/signups.html',
            {
                'signups': signups,
                'globalemails': email_used_for_signups if email_used_for_signups else None,
                'globalphones': phone_used_for_signups if email_used_for_signups else None
            }
        )
    else:
        return HttpResponseForbidden()


@login_required
def signups_settings(request):
    accountprovider, created = AccountProvider.objects.get_or_create(name='grantcoin')
    emailtemplate = ApprovedMailTemplate.objects.filter(selected=True)
    if not emailtemplate:
        default_template = True
    else:
        default_template = False
    if request.method == 'POST':
        maxdist = request.POST.get('maxdist')
        accountprovider.allowed_distance = maxdist
        accountprovider.save()
    return render(
        request,
        'autosignup/settings.html',
        {
            'accountprovider': accountprovider,
            'default_template': default_template
        }
    )


@login_required
def delete_signup(request):
    if request.method == 'POST':
        signup_id = CommunitySignup.objects.get(id=request.POST.get('signup_id'))
        signup_id.delete()
        return HttpResponse('OK')
    else:
        return HttpResponseForbidden()


@login_required
def set_signup_status(request):
    if request.method == 'POST':
        accountprovider, created = AccountProvider.objects.get_or_create(
            name='grantcoin',
        )
        status = request.POST.get('status')
        if status == 'on':
            accountprovider.signup_is_open = True
            accountprovider.save()
        if status == 'off':
            accountprovider.signup_is_open = False
            accountprovider.save()
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()


@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountAddContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return render(
                request,
                'autosignup/accountaddform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
def edit_signup(request, id):
    community_signup = CommunitySignup.objects.get(id=id)
    form = CommunitySignupForm(instance=community_signup)
    if request.method == 'POST':
        form = CommunitySignupForm(request.POST, instance=community_signup)
        if form.is_valid:
            community_signup = form.save(commit=False)
            if community_signup.status == 'approved' and not community_signup.approval_mail_sent:
                    community_signup.verified_date = now()
                    template_path = get_selected_template_path()
                    task_send_approval_mail.delay(community_signup, template_path)
            community_signup.save()
            return HttpResponse(community_signup.id)
        else:
            return render(
                request,
                'autosignup/community_signupedit.html',
                {'form': form, 'community_signup': community_signup},
                status=500
            )
    return render(
        request,
        'autosignup/community_signupedit.html',
        {'form': form, 'community_signup': community_signup}
    )


@require_POST
@login_required
def resend_approval(request):
    signup_id = request.POST.get('signup_id')
    community_signup = CommunitySignup.objects.get(id=signup_id)
    community_signup.status = 'approved'
    community_signup.approval_mail_sent = True
    community_signup.save()
    template_path = get_selected_template_path()
    task_send_approval_mail.delay(community_signup, template_path)
    return HttpResponse(status=200)


@login_required
def filter_signup(request):
    sfilter = request.GET.get('sfilter', 'pending')
    signups = CommunitySignup.objects.filter(sent_to_community_staff=True)
    signups = signups.filter(status=sfilter)
    return render(
        request,
        'autosignup/sfilter.html',
        {'signups': signups}
    )


@login_required
def search_signup(request):
    sfilter = request.GET.get('sfilter')
    username = request.GET.get('username')
    signups = CommunitySignup.objects.filter(
        sent_to_community_staff=True,
        status=sfilter,
        user__username__icontains=username
    )
    return render(
        request,
        'autosignup/sfilter.html',
        {'signups': signups}
    )


@login_required
def get_histories(request, id):
    signup = CommunitySignup.objects.get(id=id)
    histories = signup.history.all()
    return render(
        request,
        'autosignup/signuphistories.html',
        {
            'histories': histories
        }
    )


@login_required
def revert_to_history(request):
    if request.method == 'POST':
        history_id = request.POST.get('history_id')
        history_object_id = request.POST.get('history_object_id')
        signup = CommunitySignup.objects.get(id=history_object_id)
        history = signup.history.get(history_id=history_id)
        signup.useremail = history.useremail
        signup.userphone = history.userphone
        signup.useraddress_in_db = history.useraddress_in_db
        signup.status = history.status
        signup.save()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@login_required
def get_history(request, id):
    signup = CommunitySignup.objects.get(id=id)
    history = signup.history.get(id=request.GET.get('history_id'))
    return render(
        request,
        'autosignup/signuphistory.html',
        {
            'history': history
        }
    )


@require_POST
@login_required
def upload_template(request):
    accountprovider = AccountProvider.objects.get(id=request.POST.get('id'))
    template = request.FILES.get('template')
    approvedmailtemplate = ApprovedMailTemplate(
        accountprovider=accountprovider,
        template=template
    )
    templates = accountprovider.mailtemplate.all()
    for template in templates:
        template.selected = False
        template.save()
    approvedmailtemplate.selected = True
    approvedmailtemplate.save()
    return HttpResponseRedirect(reverse('autosignup:signups_settings'))


@require_POST
@login_required
def change_template(request):
    accountprovider = AccountProvider.objects.get(id=request.POST.get('id'))
    template_id = request.POST.get('template_id')
    templates = accountprovider.mailtemplate.all()
    if template_id == 'default':
        for template in templates:
            template.selected = False
            template.save()
    else:
        for template in templates:
            template.selected = False
            template.save()
        template = ApprovedMailTemplate.objects.get(id=template_id)
        template.selected = True
        template.save()
    return HttpResponse(status=200)


@login_required
def download_template(request):
    template_id = request.GET.get('template_id')
    template = ApprovedMailTemplate.objects.get(id=template_id)
    html_file_path = template.template.path
    html_file = file(html_file_path, 'r')
    html_file_downloadable = html_file.read()
    response = HttpResponse(
        html_file_downloadable,
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename="%s"' % template.filename()
    html_file.close()
    return response


@require_POST
@login_required
def delete_template(request):
    template_id = request.POST.get('template_id')
    template = ApprovedMailTemplate.objects.get(id=template_id)
    template_path = template.template.path
    os.remove(template_path)
    template.delete()
    return HttpResponse(status=200)


@require_POST
@login_required
def upload_member_csv(request):
    accountprovider = AccountProvider.objects.get(id=request.POST.get('id'))
    csv = request.FILES.get('csv')
    fetch_twilio = request.POST.get('fetch_twilio')
    accountprovidercsv = AccountProviderCSV(
        accountprovider=accountprovider,
        csv=csv
    )
    accountprovidercsv.save()
    if fetch_twilio:
        task_add_member_from_csv.delay(accountprovidercsv, fetch_twilio=True)
    else:
        task_add_member_from_csv.delay(accountprovidercsv)
    return HttpResponseRedirect(reverse('autosignup:signups_settings'))


@require_POST
@login_required
def send_member_invitation(request):
    invitation = Invitation.objects.get(id=request.POST.get('invitation_id'))
    send_csv_member_invitation_email(
        email=invitation.email,
        invitation_id=invitation.invitation_id,
        username=invitation.username,
        password=invitation.password
    )
    invitation.sent = True
    invitation.save()
    return HttpResponse(status=200)


def get_date(date_obj):
    return str(date_obj.year) + '-' + str(date_obj.month) + '-' + str(date_obj.day)


@login_required
def download_member_csv(request):
    accountprovider = AccountProvider.objects.get(id=request.GET.get('id'))
    community_signups = CommunitySignup.objects.filter(community=accountprovider.name)
    temp_csvs = []
    for community_signup in community_signups:
        temp_csv = []
        if community_signup.signup_date:
            temp_csv.append(get_date(community_signup.signup_date))
        else:
            temp_csv.append('')
        if community_signup.verified_date:
            temp_csv.append(get_date(community_signup.verified_date))
        else:
            temp_csv.append('')
        if community_signup.user.get_full_name:
            temp_csv.append(community_signup.user.get_full_name())
        else:
            temp_csv.append('')
        if community_signup.useraddress_in_db:
            temp_csv.append(community_signup.useraddress_in_db)
        else:
            temp_csv.append('')
        if community_signup.useraddress_from_twilio:
            temp_csv.append(community_signup.useraddress_from_twilio)
        else:
            temp_csv.append('')
        if community_signup.useraddress_from_twilio:
            temp_csv.append(community_signup.useraddress_from_geoip)
        else:
            temp_csv.append('')
        if community_signup.referred_by:
            temp_csv.append(community_signup.referred_by)
        else:
            temp_csv.append('')
        if community_signup.referral_code:
            temp_csv.append(community_signup.referral_code)
        else:
            temp_csv.append('')
        if community_signup.wallet_address:
            temp_csv.append(community_signup.wallet_address)
        else:
            temp_csv.append('')
        if community_signup.status:
            temp_csv.append(community_signup.status)
        else:
            temp_csv.append('')
        csv_row = ','.join(temp_csv)
        temp_csvs.append(csv_row)
    csv_f = '\n'.join(temp_csvs)
    print(csv_f)
    response = HttpResponse(
        csv_f,
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename="membercsv.csv"'
    return response
