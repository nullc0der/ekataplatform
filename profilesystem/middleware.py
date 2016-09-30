from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from profilesystem.models import UserCompletionRing


class RemoveSkippedMiddleware(object):
    def process_request(self, request):
        current_user = request.user
        if current_user.is_authenticated() and request.path == reverse('dashboard:index'):
            profile = current_user.profile
            completionring, created = \
                UserCompletionRing.objects.get_or_create(user=current_user)
            skipped_tasks = completionring.skipped_list['skipped']
            if profile.website and 'website' in skipped_tasks:
                skipped_tasks.remove('website')
            if profile.gender and 'gender' in skipped_tasks:
                skipped_tasks.remove('gender')
            if profile.avatar and 'avatar' in skipped_tasks:
                skipped_tasks.remove('avatar')
            if hasattr(current_user, 'phone') and 'phone' in skipped_tasks:
                skipped_tasks.remove('phone')
            if hasattr(current_user, 'address') and 'address' in skipped_tasks:
                skipped_tasks.remove('address')
            if current_user.socialaccount_set.all() and 'socialaccount' in skipped_tasks:
                skipped_tasks.remove('socialaccount')
            if current_user.emailaddress_set.all():
                if 'email' in skipped_tasks:
                    skipped_tasks.remove('email')
                for emailaddress in current_user.emailaddress_set.all():
                    if emailaddress.primary:
                        if emailaddress.verified and 'email_verified' in skipped_tasks:
                            skipped_tasks.remove('email_verified')
            completionring.skipped_list = {"skipped": skipped_tasks}
            completionring.save()


class CheckInvitationMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            if request.path not in [reverse('invitationsystem:addinvitation'), reverse('logout')]:
                if not request.user.profile.invitation_verified:
                    return redirect(reverse('invitationsystem:addinvitation'))
