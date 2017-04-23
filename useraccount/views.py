from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings
from useraccount.models import Transaction, UserAccount,\
    DistributeVerification, AdminDistribution, NextRelease
from autosignup.models import CommunitySignup
from useraccount.forms import TransactionForm, DistributionForm,\
    CodeVerificationForm, NextReleaseForm
from useraccount.utils import create_ekata_units_account,\
    get_ekata_units_info, send_ekata_units, request_new_address
from useraccount.tasks import task_send_distribute_phone_verfication, \
    task_dist_ekata_units
from autosignup.forms import AccountAddContactForm

# Create your views here.


@login_required
def account_page(request):
    try:
        communitysignup = CommunitySignup.objects.get(user=request.user)
    except ObjectDoesNotExist:
        communitysignup = None
    variables = {
            'communitysignup': communitysignup,
            'form': AccountAddContactForm()
        }
    return render(request, 'useraccount/index.html', context=variables)


@login_required
@require_POST
def subscribe_ekata_units(request):
    try:
        useraccount = request.user.useraccount
        message = "You've already subscribed to Ekata Units"
    except ObjectDoesNotExist:
        account_info = create_ekata_units_account(request.user)
        if account_info:
            message = "Subscribed"
        else:
            message = "Something went wrong!! Try again later"
    return JsonResponse({'message': message})


@login_required
def ekata_units_info(request):
    try:
        useraccount = request.user.useraccount
        units_info = get_ekata_units_info(request.user.username)
        if not units_info:
            variables = {
                'message': "Something went wrong!! Try again later"
            }
        else:
            variables = units_info
            variables['form'] = TransactionForm(request)
    except ObjectDoesNotExist:
        variables = {
            'message': "You've not subscribed yet"
        }
    return render(
        request,
        'useraccount/ekataunitsinfo.html',
        context=variables
    )


@login_required
@require_POST
def get_account_new_address(request):
    address = request_new_address(request.user.username)
    if not address:
        return HttpResponse(status=500)
    return HttpResponse(status=200)


@login_required
def get_ekata_units_users(request):
    res = []
    query = request.GET.get('term', '')
    users = User.objects.filter(
        username__istartswith=query).exclude(username=request.user)[:5]
    for user in users:
        res_dict = {}
        if hasattr(user, 'useraccount'):
            if user.profile.avatar:
                avatar_url = user.profile.avatar.thumbnail['30x30'].url
            else:
                avatar_url = '/static/dist/img/placeholder-user.png'
            res_dict['value'] = user.username
            res_dict['image'] = avatar_url
            res.append(res_dict)
    return JsonResponse(res, safe=False)


@require_POST
@login_required
def transfer_ekata_units(request):
    form = TransactionForm(request, request.POST)
    if form.is_valid():
        res = send_ekata_units(
            from_user=request.user.username,
            to_user=form.cleaned_data.get('reciever'),
            amount=form.cleaned_data.get('units')
        )
        if res:
            return HttpResponse(_('Transferred {0} units to {1}'.format(
                form.cleaned_data.get('units'),
                form.cleaned_data.get('reciever')
            )))
        else:
            form.add_error(
                field=None, error=_('Error processing!! Try later')
            )
    return render(
        request,
        'useraccount/transferform.html',
        {'form': form},
        status=500
    )


@user_passes_test(lambda u: u.is_staff)
def ekata_units_admin(request):
    units_info = get_ekata_units_info("")
    total_account = UserAccount.objects.count()
    lastdistributions = AdminDistribution.objects.all()
    if not units_info:
        variables = {
            'message': "Something is wrong!! Try again later"
        }
    else:
        variables = units_info
        variables['total_account'] = total_account
        variables['form'] = DistributionForm()
        variables['nrform'] = NextReleaseForm(
            instance=NextRelease.objects.latest())
        variables['lastdistributions'] = lastdistributions
    return render(
        request,
        'useraccount/ekataunitsadmin.html',
        context=variables
    )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def distribute_ekata_units(request):
    form = DistributionForm(request.POST)
    if form.is_valid():
        code = get_random_string(length=8, allowed_chars='0123456789')
        distcode = DistributeVerification(
            user=request.user,
            code=code
        )
        distcode.save()
        task_send_distribute_phone_verfication.delay(
            settings.EKATA_UNITS_VERIFY_NO, distcode.code)
        vform = CodeVerificationForm(
            initial={'amount': form.cleaned_data['amount']})
        return render(
            request,
            'useraccount/verificationform.html',
            {
                'form': vform,
                'phone_no': settings.EKATA_UNITS_VERIFY_NO
            }
        )
    return render(
        request,
        'useraccount/distributeform.html',
        {
            'form': form
        },
        status=500
    )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def verify_dist_code(request):
    form = CodeVerificationForm(request.POST)
    if form.is_valid():
        task_dist_ekata_units.delay(form.cleaned_data['amount'])
        return HttpResponse(status=200)
    return render(
        request,
        'useraccount/verificationform.html',
        {
            'form': form
        },
        status=500
    )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def add_next_release(request):
    form = NextReleaseForm(request.POST, instance=NextRelease.objects.latest())
    if form.is_valid():
        form.save()
        return HttpResponse(status=200)
    return render(
        request,
        'useraccount/nextreleaseform.html',
        {
            'nrform': form
        },
        status=500
    )
