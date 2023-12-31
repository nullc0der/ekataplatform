import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.template import loader

from eblast.models import EmailGroup, EmailId, EmailTemplate,\
 EmailCampaign, CampaignTracking
from eblast.forms import EmailGroupForm, EmailTemplateForm,\
 EmailTemplateEditForm, EmailCampaignForm, EmailTestSendForm, EmailSendForm,\
 EmailCampaignEditForm, EmailGroupAddUserForm, EmailGroupCSVForm
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
                'userform': EmailGroupAddUserForm(instance=emailgroup),
                'csvform': EmailGroupCSVForm(instance=emailgroup)
            }
        )
    return render(
        request,
        'eblast/emailgroups_page.html',
        {
            'form': EmailGroupForm(),
            'userform': EmailGroupAddUserForm(instance=emailgroup) if emailgroup else EmailGroupAddUserForm(),
            'csvform': EmailGroupCSVForm(instance=emailgroup) if emailgroup else EmailGroupCSVForm(),
            'emailgroups': emailgroups,
        }
    )


@user_passes_test(lambda u: u.is_staff)
def create_emailgroup(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST, request.FILES)
        if form.is_valid():
            emailgroup = form.save()
            template = loader.get_template('eblast/singleemailgrouplist.html')
            context = {'emailgroup': emailgroup}
            html = template.render(context)
            response_dict = {
                'id': emailgroup.id,
                'html': html
            }
            data = json.dumps(response_dict)
            return HttpResponse(data, 'application/json')
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
def add_user_to_emailgroup(request, id):
    emailgroup = EmailGroup.objects.get(id=id)
    form = EmailGroupAddUserForm(request.POST, instance=emailgroup)
    if form.is_valid():
        emailgroup = form.save()
        return HttpResponse(emailgroup.id)
    else:
        return render(
            request,
            'eblast/addrecipient.html',
            {
                'emailgroup': emailgroup,
                'userform': form
            },
            status=500
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def add_csv_to_emailgroup(request, id):
    emailgroup = EmailGroup.objects.get(id=id)
    form = EmailGroupCSVForm(request.POST, request.FILES, instance=emailgroup)
    if form.is_valid():
        emailgroup = form.save()
        return HttpResponse(emailgroup.id)
    else:
        return render(
            request,
            'eblast/addcsv.html',
            {
                'emailgroup': emailgroup,
                'csvform': form
            },
            status=500
        )


@require_POST
@user_passes_test(lambda u: u.is_staff)
def change_group_name(request):
    emailgroup = EmailGroup.objects.get(id=request.POST.get('id'))
    emailgroup.name = request.POST.get('name')
    emailgroup.save()
    return HttpResponse(status=200)


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
def filter_groups(request):
    emailgroups = EmailGroup.objects.filter(name__icontains=request.GET.get('query'))
    return render(
        request,
        'eblast/emailgroupslist.html',
        {
            'emailgroups': emailgroups
        }
    )


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
            template = loader.get_template('eblast/singletemplatelist.html')
            context = {'emailtemplate': emailtemplate}
            html = template.render(context)
            response_dict = {
                'id': emailtemplate.id,
                'html': html
            }
            data = json.dumps(response_dict)
            return HttpResponse(data, 'application/json')
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


@require_POST
@user_passes_test(lambda u: u.is_staff)
def change_template_name(request):
    emailtemplate = EmailTemplate.objects.get(id=request.POST.get('id'))
    emailtemplate.name = request.POST.get('name')
    emailtemplate.save()
    return HttpResponse(status=200)


@user_passes_test(lambda u: u.is_staff)
def filter_template(request):
    emailtemplates = EmailTemplate.objects.filter(name__icontains=request.GET.get('query'))
    return render(
        request,
        'eblast/emailtemplateslist.html',
        {
            'emailtemplates': emailtemplates
        }
    )


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
                'form': EmailCampaignEditForm(instance=emailcampaign),
                'testform': EmailTestSendForm(),
                'sendform': EmailSendForm()
            }
        )
    return render(
        request,
        'eblast/emailcampaign_page.html',
        {
            'form': EmailCampaignEditForm(instance=emailcampaign) if emailcampaign else EmailCampaignForm(),
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
            template = loader.get_template('eblast/singlecampaignlist.html')
            context = {'emailcampaign': emailcampaign}
            html = template.render(context)
            response_dict = {
                'id': emailcampaign.id,
                'html': html
            }
            data = json.dumps(response_dict)
            return HttpResponse(data, 'application/json')
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
    form = EmailCampaignEditForm(request.POST, instance=emailcampaign)
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


@require_POST
@user_passes_test(lambda u: u.is_staff)
def change_campaign_name(request):
    emailcampaign = EmailCampaign.objects.get(id=request.POST.get('id'))
    emailcampaign.campaign_name = request.POST.get('name')
    emailcampaign.save()
    return HttpResponse(status=200)


@user_passes_test(lambda u: u.is_staff)
def filter_campaign(request):
    filters_enabled = request.GET.getlist('filters_enabled')
    if 'sent' in filters_enabled:
        emailcampaigns = EmailCampaign.objects.filter(draft=False)
    if 'draft' in filters_enabled:
        emailcampaigns = EmailCampaign.objects.filter(draft=True)
    if 'sent' in filters_enabled and 'draft' in filters_enabled:
        emailcampaigns = EmailCampaign.objects.all()
    if 'query' in request.GET:
        query = request.GET.get('query')
        emailcampaigns = emailcampaigns.filter(campaign_name__icontains=query)
    return render(
        request,
        'eblast/emailcampaignlist.html',
        {
            'emailcampaigns': emailcampaigns
        }
    )
