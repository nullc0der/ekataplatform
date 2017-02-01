import requests

from django.contrib.auth.models import User
from django.core import serializers
from eblast.models import EmailGroup


def create_emailgroup(basicgroup):
    emailgroup, created = EmailGroup.objects.get_or_create(
        name=basicgroup.name,
        basic_group=basicgroup
    )
    for user in basicgroup.super_admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.moderators.all():
        emailgroup.users.add(user)
    for user in basicgroup.members.all():
        emailgroup.users.add(user)

    return 1


def send_serialized_user(pk_set):
    users = User.objects.filter(id__in=pk_set)
    data = serializers.serialize('json', users)
    payload = {'data': data}
    url = 'http://localhost:8001/en/type/integrate_users/'
    res = requests.post(url, data=payload)
    return res.status_code
