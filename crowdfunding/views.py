import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from crowdfunding.models import CrowdFund, PredefinedAmount, ProductFeature
from crowdfunding.forms import PaymentForm, AdminForm, PredefinedAmountForm,\
    ProductFeatureForm
from stripepayment.utils import StripePayment
from stripepayment.models import Payment

# Create your views here.


@login_required
def index(request):
    percent_raised = 0
    default_amount = 20
    try:
        crowdfund = CrowdFund.objects.latest()
        default_amount = crowdfund.predefinedamount_set.filter(default=True)
        if len(default_amount):
            default_amount = default_amount[0].amount
        else:
            default_amount = 20
        if crowdfund.raised:
            percent_raised = int((crowdfund.raised * 100.0) / crowdfund.goal)
    except ObjectDoesNotExist:
        crowdfund = None
    return render(
        request,
        'crowdfunding/index.html',
        {
            'crowdfund': crowdfund,
            'percent_raised': percent_raised,
            'default_amount': default_amount
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
                'crowdfunding/thankyou.html',
                {
                    'crowdfund': crowdfund
                }
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
    pform = PredefinedAmountForm()
    fform = ProductFeatureForm()
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
            'pform': pform,
            'fform': fform,
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


@user_passes_test(lambda u: u.is_staff)
@require_POST
def add_predefined_amount(request):
    form = PredefinedAmountForm(request.POST)
    if form.is_valid():
        predefined_amount = form.save(commit=False)
        crowdfund = CrowdFund.objects.latest()
        predefined_amount.crowdfund = crowdfund
        if predefined_amount.default:
            for i in PredefinedAmount.objects.filter(default=True):
                i.default = False
                i.save()
        predefined_amount.save()
        return HttpResponse(status=200)
    else:
        return render(
            request,
            'crowdfunding/paymentamountform.html',
            {
                'pform': form
            },
            status=500
        )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def add_product_feature(request):
    form = ProductFeatureForm(request.POST)
    if form.is_valid():
        product_feature = form.save(commit=False)
        crowdfund = CrowdFund.objects.latest()
        product_feature.crowdfund = crowdfund
        product_feature.save()
        return render(
            request,
            'crowdfunding/singlefeature.html',
            {
                'feature': product_feature
            }
        )
    else:
        return render(
            request,
            'crowdfunding/productfeatureform.html',
            {
                'fform': form
            },
            status=500
        )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_product_feature(request):
    product_feature = ProductFeature.objects.get(id=request.POST.get('id'))
    product_feature.delete()
    return HttpResponse(status=200)
