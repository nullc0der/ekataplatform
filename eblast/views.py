from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now

from eblast.models import EmailGroup, EmailId, EmailTemplate, EmailCampaign, CampaignTracking
from eblast.forms import EmailGroupForm, EmailTemplateForm,\
 EmailTemplateEditForm, EmailCampaignForm, EmailTestSendForm, EmailSendForm
from eblast.tasks import task_send_test_mail, task_send_campaign_email
# Create your views here.


@user_passes_test(lambda u: u.is_staff)
def emailgroups_page(request):
    emailgroups = EmailGroup.objects.all()
    if emailgroups:
        emailgroup = emailgroups[0]
    else:
        emailgroup = None
    if 'emailgroup' in request.GET:
        emailgroup = EmailGroup.objects.get(id=request.GET.get('emailgroup'))
        return render(
            request,
            'eblast/emailgroup.html',
            {
                'emailgroup': emailgroup,
                'form': EmailGroupForm(instance=emailgroup)
            }
        )
    return render(
        request,
        'eblast/emailgroups_page.html',
        {
            'form': EmailGroupForm(instance=emailgroup) if emailgroups else EmailGroupForm(),
            'emailgroups': emailgroups,
        }
    )


@user_passes_test(lambda u: u.is_staff)
def create_emailgroup(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST, request.FILES)
        if form.is_valid():
            emailgroup = form.save()
            return HttpResponse(emailgroup.id)
        else:
            return render(
                request,
                'eblast/emailgroupform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return render(
            request,
            'eblast/emailgroupform.html',
            {
                'form': EmailGroupForm()
            }
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def delete_emailgroup(request):
    emailgroup = EmailGroup.objects.get(id=request.POST.get('id'))
    emailgroup.delete()
    return HttpResponse(status=200)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def edit_emailgroup(request, id):
    emailgroup = EmailGroup.objects.get(id=id)
    form = EmailGroupForm(request.POST, request.FILES, instance=emailgroup)
    if form.is_valid():
        emailgroup = form.save()
        return HttpResponse(emailgroup.id)
    else:
        return render(
            request,
            'eblast/emailgroupedit.html',
            {
                'emailgroup': emailgroup,
                'form': EmailGroupForm(instance=emailgroup)
            },
            status=500
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def remove_emailid(request):
    email_id = EmailId.objects.get(id=request.POST.get('id'))
    email_id.delete()
    return HttpResponse(status=200)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def unsubscribe_emailid(request):
    email_id = EmailId.objects.get(id=request.POST.get('id'))
    email_id.send_email_from_group = False
    email_id.save()
    return HttpResponse(status=200)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def subscribe_emailid(request):
    email_id = EmailId.objects.get(id=request.POST.get('id'))
    email_id.send_email_from_group = True
    email_id.save()
    return HttpResponse(status=200)


@user_passes_test(lambda u: u.is_staff)
def emailtemplates_page(request):
    emailtemplates = EmailTemplate.objects.all()
    if emailtemplates:
        emailtemplate = emailtemplates[0]
    else:
        emailtemplate = None
    if 'emailtemplate' in request.GET:
        emailtemplate = EmailTemplate.objects.get(id=request.GET.get('emailtemplate'))
        return render(
            request,
            'eblast/emailtemplate.html',
            {
                'emailtemplate': emailtemplate,
                'form': EmailTemplateEditForm(instance=emailtemplate)
            }
        )
    return render(
        request,
        'eblast/emailtemplates_page.html',
        {
            'form': EmailTemplateEditForm(instance=emailtemplate) if emailtemplate else EmailTemplateForm(),
            'emailtemplates': emailtemplates,
        }
    )


@user_passes_test(lambda u: u.is_staff)
def add_emailtemplate(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            emailtemplate = form.save()
            return HttpResponse(emailtemplate.id)
        else:
            return render(
                request,
                'eblast/emailtemplateform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return render(
            request,
            'eblast/emailtemplateform.html',
            {
                'form': EmailTemplateForm()
            }
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def delete_emailtemplate(request):
    emailtemplate = EmailTemplate.objects.get(id=request.POST.get('id'))
    emailtemplate.delete()
    return HttpResponse(status=200)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def edit_emailtemplate(request, id):
    emailtemplate = EmailTemplate.objects.get(id=id)
    form = EmailTemplateEditForm(request.POST, request.FILES, instance=emailtemplate)
    if form.is_valid():
        emailtemplate = form.save()
        return HttpResponse(emailtemplate.id)
    else:
        return render(
            request,
            'eblast/emailtemplateedit.html',
            {
                'emailtemplate': emailtemplate,
                'form': form
            },
            status=500
        )


@user_passes_test(lambda u: u.is_staff)
def preview_emailtemplate(request, id):
    emailtemplate = EmailTemplate.objects.get(id=id)
    return HttpResponse(emailtemplate.template)


@user_passes_test(lambda u: u.is_staff)
def emailcampaign_page(request):
    emailcampaigns = EmailCampaign.objects.all()
    if emailcampaigns:
        emailcampaign = emailcampaigns[0]
    else:
        emailcampaign = None
    if 'emailcampaign' in request.GET:
        emailcampaign = EmailCampaign.objects.get(id=request.GET.get('emailcampaign'))
        return render(
            request,
            'eblast/emailcampaign.html',
            {
                'emailcampaign': emailcampaign,
                'form': EmailCampaignForm(instance=emailcampaign),
                'testform': EmailTestSendForm(),
                'sendform': EmailSendForm()
            }
        )
    return render(
        request,
        'eblast/emailcampaign_page.html',
        {
            'form': EmailCampaignForm(instance=emailcampaign) if emailcampaign else EmailCampaignForm(),
            'emailcampaigns': emailcampaigns,
            'testform': EmailTestSendForm(),
            'sendform': EmailSendForm()
        }
    )


@user_passes_test(lambda u: u.is_staff)
def add_emailcampaign(request):
    if request.method == 'POST':
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            emailcampaign = form.save()
            return HttpResponse(emailcampaign.id)
        else:
            return render(
                request,
                'eblast/emailcampaignform.html',
                {
                    'form': form
                },
                status=500
            )
    else:
        return render(
            request,
            'eblast/emailcampaignform.html',
            {
                'form': EmailCampaignForm
            }
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def edit_emailcampaign(request, id):
    emailcampaign = EmailCampaign.objects.get(id=id)
    form = EmailCampaignForm(request.POST, instance=emailcampaign)
    if form.is_valid():
        emailcampaign = form.save()
        return HttpResponse(emailcampaign.id)
    else:
        return render(
            request,
            'eblast/editemailcampaign.html',
            {
                'emailcampaign': emailcampaign,
                'form': form
            },
            status=500
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def delete_emailcampaign(request):
    emailcampaign = EmailCampaign.objects.get(id=request.POST.get('id'))
    emailcampaign.delete()
    return HttpResponse(status=200)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def test_send_campaign(request, id):
    if request.method == 'POST':
        form = EmailTestSendForm(request.POST)
        if form.is_valid():
            task_send_test_mail.delay(
                id,
                form.cleaned_data.get('from_email_id'),
                form.cleaned_data.get('test_email')
            )
            return HttpResponse(status=200)
        else:
            return render(
                request,
                'eblast/testsendmailform.html',
                {
                    form: form
                },
                status=500
            )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def send_campaign(request, id):
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            campaign = EmailCampaign.objects.get(id=id)
            campaign.draft = False
            campaign.save()
            task_send_campaign_email.delay(
                id,
                form.cleaned_data.get('from_email_id'),
                form.cleaned_data.get('to_groups')
            )
            return HttpResponse(status=200)
        else:
            return render(
                request,
                'eblast/sendmailform.html',
                {
                    form: form
                },
                status=500
            )


def view_email_in_browser(request, id):
    emailcampaign = get_object_or_404(EmailCampaign, id=id)
    message = emailcampaign.message
    return HttpResponse(message)


def get_campaign_image_link(request, campaign_id, reciever_id):
    url = 'https://google.co.in'
    campaign = EmailCampaign.objects.filter(tracking_id=campaign_id)
    tracking = CampaignTracking.objects.filter(tracking_id=reciever_id)
    if tracking:
        tracking = tracking[0]
        tracking.opened = True
        tracking.opened_at = now()
        tracking.save()
    return HttpResponse(url)


@user_passes_test(lambda u: u.is_staff)
def campaign_tracking_data(request):
    campaign = EmailCampaign.objects.get(id=request.GET.get('id'))
    trackings = campaign.trackings.all()
    opened = trackings.filter(opened=True).count()
    sent = trackings.count()
    return render(
        request,
        'eblast/tracking_data.html',
        {
            'opened': opened,
            'sent': sent,
            'campaign': campaign
        }
    )
