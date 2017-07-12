from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.signals import user_logged_in
from useractivity.models import FlaggedAccount


@receiver(user_logged_in)
def delete_flagged_account(request, user, **kwargs):
    try:
        flaggedaccount = FlaggedAccount.objects.get(user=user)
        flaggedaccount.delete()
    except ObjectDoesNotExist:
        pass
