import requests
import json
from django.conf import settings

from taigaissuecreator.models import TaigaIssue

API_BASE_URL = 'https://taiga.ekata.social/api/v1'
LOGIN_URL = API_BASE_URL + '/auth'
ISSUE_URL = API_BASE_URL + '/issues'


def get_auth_token():
    """ Returns auth_token if success else None """
    data = {
        'username': settings.TAIGA_USERNAME,
        'password': settings.TAIGA_PASSWORD,
        'type': 'normal'
    }
    login_res = requests.post(LOGIN_URL, data=data)
    if login_res.status_code == 200:
        res_data = json.loads(login_res.content)
        if res_data['auth_token']:
            return res_data['auth_token']
    return None


def post_issue(posted_by, subject, description):
    auth_token = get_auth_token()
    taigaissue = TaigaIssue(
        posted_by=posted_by,
        subject=subject,
        description=description
    )
    public_profile_chunk = posted_by.profile.get_public_profile_url().split(
        '/')[2:]
    public_profile = \
        "https://development.ekata.social/"\
        + '/'.join(public_profile_chunk)
    extra_info = \
        '\n\n\n####Extra Info\n Original Creator:' + \
        '%s\n User ID: %s\n Profile url: %s'\
        % (
            posted_by.username,
            posted_by.id,
            public_profile
        )
    if auth_token:
        headers = {
            "Authorization": "Bearer " + auth_token
        }
        data = {
            'subject': subject,
            'description': description + extra_info,
            'project': 2
        }
        issue_res = requests.post(ISSUE_URL, headers=headers, data=data)
        taigaissue.posted = True
    taigaissue.save()
