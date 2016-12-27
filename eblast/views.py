from django.shortcuts import render

from eblast.models import EmailGroup, EmailId, EmailTemplate, EmailCampaign
# Create your views here.


def emailgroups_page(request):
    return render(
        request,
        'eblast/emailgroups_page.html'
    )
