from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from sysadmin.models import EmailUpdate

# Create your views here.


def view_email_in_browser(request, id):
    emailupdate = get_object_or_404(EmailUpdate, id=id)
    message = emailupdate.message
    return HttpResponse(message)
