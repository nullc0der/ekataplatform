import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from crowdfunding.models import CrowdFund
from crowdfunding.forms import PaymentForm, AdminForm
from stripepayment.utils import StripePayment
from stripepayment.models import Payment

# Create your views here.


@login_required
def index(request):
    percent_raised = 0
    try:
        crowdfund = CrowdFund.objects.latest()
        if crowdfund.raised:
            percent_raised = int((crowdfund.raised * 100.0) / crowdfund.goal)
    except ObjectDoesNotExist:
        crowdfund = None
    return render(
        request,
        'crowdfunding/index.html',
        {
            'crowdfund': crowdfund,
            'percent_raised': percent_raised
        }
    )


@login_required
@require_POST
def accept_payment(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        stripepayment = StripePayment(user=request.user)
        payment_success = stripepayment.process_payment(
            token=request.POST['stripeToken'],
            payment_type='crowdfund',
            amount=int(request.POST['amount']),
            message=request.POST['message']
        )
        if payment_success:
            try:
                crowdfund = CrowdFund.objects.latest()
                if crowdfund.raised:
                    crowdfund.raised += int(request.POST['amount'])
                else:
                    crowdfund.raised = int(request.POST['amount'])
                if crowdfund.raised >= crowdfund.goal:
                    crowdfund.active = False
                crowdfund.save()
            except ObjectDoesNotExist:
                pass
            return render(
                request,
                'crowdfunding/thankyou.html'
            )
        else:
            return HttpResponse(
                json.dumps({
                    '__all__': 'Error processing! try again later'
                }),
                status=500
            )
    else:
        return HttpResponse(json.dumps(form.errors), status=500)


@user_passes_test(lambda u: u.is_staff)
def crowdfund_admin(request):
    form = AdminForm()
    percent_raised = 0
    try:
        crowdfund = CrowdFund.objects.latest()
        form = AdminForm(instance=crowdfund)
        if crowdfund.raised:
            percent_raised = int((crowdfund.raised * 100.0) / crowdfund.goal)
    except ObjectDoesNotExist:
        crowdfund = None
    payments = Payment.objects.filter(payment_type='crowdfund')
    return render(
        request,
        'crowdfunding/admin.html',
        {
            'form': form,
            'crowdfund': crowdfund,
            'percent_raised': percent_raised,
            'payments': payments
        },
    )


@user_passes_test(lambda u: u.is_staff)
def start_crowdfund(request):
    form = AdminForm()
    return render(
        request,
        'crowdfunding/update_crowdfund.html',
        {
            'form': form
        }
    )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def update_crowdfund(request):
    form = AdminForm(request.POST)
    try:
        crowdfund = CrowdFund.objects.latest()
        form = AdminForm(request.POST, instance=crowdfund)
    except ObjectDoesNotExist:
        pass
    if form.is_valid():
        form.save()
        return HttpResponse(status=200)
    else:
        return render(
            request,
            'crowdfunding/update_crowdfund.html',
            {
                'form': form
            },
            status=500
        )


@user_passes_test(lambda u: u.is_staff)
def payment_details(request):
    paymentid = request.GET.get('id')
    payment = Payment.objects.get(id=paymentid)
    return render(
        request,
        'crowdfunding/payment_details.html',
        {
            'payment': payment
        }
    )
