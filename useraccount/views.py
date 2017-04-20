from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from useraccount.models import Transaction, IncomeRelease, UserAccount
from autosignup.models import CommunitySignup
from usertimeline.models import UserTimeline
from useraccount.forms import TransactionForm, RequestForm
from useraccount.utils import create_ekata_units_account, get_ekata_units_info, \
    dist_ekata_units, send_ekata_units, request_new_address
from autosignup.forms import AccountAddContactForm
from notification.utils import create_notification

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
            message = "Something is wrong!! Try again later"
    return JsonResponse({'message': message})


@login_required
def ekata_units_info(request):
    try:
        useraccount = request.user.useraccount
        units_info = get_ekata_units_info(request.user.username)
        if not units_info:
            variables = {
                'message': "Something is wrong!! Try again later"
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
        if hasattr(user, 'useraccount'):
            res.append(user.username)
    return JsonResponse(res, safe=False)


@require_POST
@login_required
def transfer_ekata_units(request):
    form = TransactionForm(request, request.POST)
    if form.is_valid():
        res = send_ekata_units(
            from_user=request.user.username,
            to_user=form.cleaned_data.get('reciever'),
            amount=form.cleaned_data.get('units'),
            instruction=form.cleaned_data.get('instruction')
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
    if not units_info:
        variables = {
            'message': "Something is wrong!! Try again later"
        }
    else:
        variables = units_info
    return render(
        request,
        'useraccount/ekataunitsadmin.html',
        context=variables
    )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def distribute_ekata_units(request):
    amount = request.POST.get('amount')
    dist_ekata_units(amount)
    return HttpResponse(status=200)


@login_required
def transfer_page(request):
    transactions = Transaction.objects.filter(to_user=request.user)
    dup = []
    transactions_list = []
    for transaction in transactions:
        if transaction.from_user.username not in dup:
            transactions_list.append(transaction)
            dup.append(transaction.from_user.username)
        if len(transactions_list) == 5:
            break
    if 'userquery' in request.GET:
        userquery = request.GET.get('userquery')
        if userquery:
            users = User.objects.filter(username__istartswith=userquery).exclude(username=request.user)[:5]
        return render(request, 'useraccount/users.html', {'users': users})
    return render(request, 'useraccount/transfer.html', {'senders': transactions_list})


@login_required
def transferunit(request, id):
    user = User.objects.get(id=id)
    form = TransactionForm(request)
    if request.method == 'POST' and request.is_ajax():
        form = TransactionForm(request, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.to_user = user
            transaction.from_user = request.user
            transaction.save()
            calculate_balance(request.user, user, form.cleaned_data['units'])
            sendertimeline = UserTimeline(
                user=request.user,
                timeline_type=1,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id,
                instruction=form.cleaned_data['instruction'],
                amount=form.cleaned_data['units']
            )
            sendertimeline.save()
            recievertimeline = UserTimeline(
                user=user,
                timeline_type=1,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=user.username,
                reciever_id=user.id,
                instruction=form.cleaned_data['instruction'],
                amount=form.cleaned_data['units']
            )
            recievertimeline.save()
            create_notification(
                user=user,
                ntype=1,
                sender=request.user.username,
                sender_id=request.user.id,
                amount=form.cleaned_data['units'],
                timeline_id=recievertimeline.id
            )
            if 'timeline' in request.POST:
                timeline_id = request.POST.get('timeline')
                try:
                    timeline = UserTimeline.objects.get(id=timeline_id)
                    timeline.not_completed = False
                    timeline.save()
                except ObjectDoesNotExist:
                    pass
            return HttpResponse(_('Transfer completed!!'))
        else:
            return render(
                request,
                'useraccount/transferform.html',
                {'form': form},
                status=500
            )
    return render(
        request,
        'useraccount/transferunit.html',
        {
            'user': user,
            'form': form
        }
    )


def calculate_balance(from_user, to_user, amount):
    from_user_account = from_user.useraccount
    to_user_account = to_user.useraccount
    to_user_account.balance += amount
    from_user_account.balance -= amount
    from_user_account.save()
    to_user_account.save()


@login_required
def requestunit(request, id):
    reciever = User.objects.get(id=id)
    form = RequestForm()
    if request.method == 'POST' and request.is_ajax():
        form = RequestForm(request.POST)
        if form.is_valid():
            unitrequest = form.save(commit=False)
            unitrequest.reciever = reciever
            unitrequest.sender = request.user
            unitrequest.save()
            sendertimeline = UserTimeline(
                user=request.user,
                timeline_type=2,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=reciever.username,
                reciever_id=reciever.id,
                instruction=form.cleaned_data['instruction'],
                amount=form.cleaned_data['units']
            )
            sendertimeline.save()
            recievertimeline = UserTimeline(
                user=reciever,
                timeline_type=2,
                sender=request.user.username,
                sender_id=request.user.id,
                reciever=reciever.username,
                reciever_id=reciever.id,
                instruction=form.cleaned_data['instruction'],
                amount=form.cleaned_data['units']
            )
            recievertimeline.save()
            create_notification(
                user=reciever,
                ntype=2,
                sender=request.user.username,
                sender_id=request.user.id,
                amount=form.cleaned_data['units'],
                timeline_id=recievertimeline.id
            )
            return HttpResponse(_('Request Sent!!'))
        else:
            return render(
                request,
                'useraccount/requestform.html',
                {'rform': form},
                status=500
            )
