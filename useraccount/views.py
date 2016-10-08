from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from useraccount.models import Transaction, IncomeRelease, UserAccount
from usertimeline.models import UserTimeline
from useraccount.forms import TransactionForm, RequestForm
from notification.utils import create_notification

# Create your views here.


@login_required
def account_page(request):
    transactions = Transaction.objects.filter(
        Q(to_user=request.user) | Q(from_user=request.user)
    ).order_by('-date')
    relaeses = IncomeRelease.objects.filter(user=request.user)
    useraccount, created = UserAccount.objects.get_or_create(user=request.user)
    next_release = useraccount.next_release
    if transactions:
        variables = {
            'next_release': next_release,
            'transactions': transactions,
            'first': transactions[0],
            'releases': relaeses
        }
    else:
        variables = {
            'next_release': next_release,
            'transactions': transactions,
            'releases': relaeses
        }
    return render(request, 'useraccount/index.html', context=variables)


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
