import json
from datetime import date, timedelta

from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from crowdfunding.models import CrowdFund, PredefinedAmount, ProductFeature
from landing.models import OgTagLink
from landing.forms import GlobalOgTagForm
from crowdfunding.forms import PaymentForm, AdminForm, PredefinedAmountForm,\
    ProductFeatureForm, CardsVideoForm, CardsImageForm
from stripepayment.utils import StripePayment
from stripepayment.models import Payment

# Create your views here.


def index(request):
    percent_raised = 0
    default_amount = 20
    ogtag = None
    crowdfund_ogtag = OgTagLink.objects.filter(
        page='crowdfunding').order_by('-id')
    if crowdfund_ogtag:
        ogtag = crowdfund_ogtag[0].globalogtag
    try:
        crowdfund = CrowdFund.objects.latest()
        damount = crowdfund.predefinedamount_set.filter(default=True)
        if len(damount):
            default_amount = damount[0].amount
        if crowdfund.raised:
            percent_raised = int((crowdfund.raised * 100.0) / crowdfund.goal)
    except ObjectDoesNotExist:
        crowdfund = None
    context = {
        'crowdfund': crowdfund,
        'percent_raised': percent_raised,
        'default_amount': default_amount,
        'ogtag': ogtag
    }
    if request.user.is_authenticated():
        return render(
            request,
            'crowdfunding/index.html',
            context=context
        )
    return render(
        request,
        'crowdfunding/public_index.html',
        context=context
    )


@require_POST
def accept_payment(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        if request.user.is_authenticated():
            stripepayment = StripePayment(
                user=request.user, fullname=request.user.get_full_name())
        elif request.POST['fullname']:
            stripepayment = StripePayment(fullname=request.POST['fullname'])
        else:
            stripepayment = StripePayment()
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
    vform = CardsVideoForm()
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
            'vform': vform,
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
        feature_name = form.cleaned_data.get('name').split()
        product_feature.linked_card = '-'.join(feature_name)\
            + '-' + get_random_string(allowed_chars='0123456789', length=4)
        product_feature.save()
        return render(
            request,
            'crowdfunding/product_features_admin.html',
            {
                'crowdfund': crowdfund
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


@user_passes_test(lambda u: u.is_staff)
@require_POST
def upload_video(request):
    crowdfund = CrowdFund.objects.latest()
    form = CardsVideoForm(request.POST, request.FILES)
    if form.is_valid():
        cards_video = form.save(commit=False)
        cards_video.crowdfund = crowdfund
        cards_video.save()
        res = {
            'cover': cards_video.cover.url,
            'video': cards_video.video.url
        }
        return HttpResponse(json.dumps(res))
    else:
        return render(
            request,
            'crowdfunding/headervideoform.html',
            {
                'vform': form
            },
            status=500
        )


@user_passes_test(lambda u: u.is_staff)
@require_POST
def upload_image(request):
    crowdfund = CrowdFund.objects.latest()
    form = CardsImageForm(request.POST, request.FILES)
    if form.is_valid():
        cards_image = form.save(commit=False)
        cards_image.crowdfund = crowdfund
        cards_image.save()
        res = {
            'image': cards_image.image.url
        }
        return HttpResponse(json.dumps(res))
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff)
@require_POST
def update_cards_html(request):
    try:
        crowdfund = CrowdFund.objects.latest()
        crowdfund.cards_html = request.POST.get('html')
        crowdfund.admin_cards_html = request.POST.get('admin_html')
        crowdfund.header_html = request.POST.get('header_html')
        crowdfund.save()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)


@user_passes_test(lambda u: u.is_staff)
def add_meta_tags(request):
    ogtaglink, created = OgTagLink.objects.get_or_create(page='crowdfunding')
    form = GlobalOgTagForm(instance=ogtaglink.globalogtag)
    if request.method == 'POST':
        form = GlobalOgTagForm(request.POST, request.FILES,
                               instance=ogtaglink.globalogtag)
        if form.is_valid():
            global_ogtag = form.save()
            ogtaglink.globalogtag = global_ogtag
            ogtaglink.save()
            return HttpResponse(status=200)
        else:
            return render(
                request,
                'crowdfunding/ogtagform.html',
                {
                    'form': form
                },
                status=500
            )
    return render(
        request,
        'crowdfunding/ogtagform.html',
        {
            'form': form
        }
    )
