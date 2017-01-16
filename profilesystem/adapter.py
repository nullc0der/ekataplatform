import requests
import tempfile

from django.core import files
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


def download_file_from_url(url):
    try:
        request = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        return None
    if request.status_code != requests.codes.ok:
        return None
    lf = tempfile.NamedTemporaryFile()
    for block in request.iter_content(1024 * 8):
        if not block:
            break
        lf.write(block)
    return files.File(lf)


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(
            request,
            sociallogin,
            form
        )
        url = sociallogin.account.get_avatar_url()
        avatar = download_file_from_url(url)
        if avatar:
            profile = user.profile
            profile.avatar.save('%s_avatar.jpg' % user.username, avatar)
        return user
