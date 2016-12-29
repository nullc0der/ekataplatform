from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

from eblast.models import EmailGroup, EmailId, EmailTemplate, EmailCampaign
from eblast.forms import EmailGroupForm
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
