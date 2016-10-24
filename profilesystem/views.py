from random import randint

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.core.cache import cache
from django.conf import settings as s
from .forms import UserForm, PInfoForm, PhoneForm, AddressForm
from .models import \
    UserProfile, UserDocuments, UserCompletionRing, UserUIState, \
    UserOneSignal, ReadSysUpdate

# Create your views here

IMAGE_EXTENSION = ['jpg', 'png', 'gif']


@login_required
def index_page(request):
    variables = {}
    social_accounts = request.user.socialaccount_set.all()
    usercomplete, created = \
        UserCompletionRing.objects.get_or_create(user=request.user)
    completed, completed_list, not_completed, not_completed_list, emailadd = \
        usercomplete.calculate_completed()
    not_verified, not_verified_tasks = usercomplete.calculate_verified()
    task_list = not_completed_list + not_verified_tasks
    if task_list:
        rand = randint(0, len(task_list) - 1)
        ncompleted = task_list[rand]
        variables['ncompleted'] = ncompleted
    if social_accounts:
        variables['show_unlink'] = True
        variables['emailadd'] = emailadd
    else:
        variables['show_unlink'] = False
        variables['emailadd'] = emailadd
    return render(
        request,
        'profilesystem/index.html',
        context=variables
    )


@login_required
def social_account_page(request):
    variables = {}
    user = request.user
    social_accounts = request.user.socialaccount_set.all()
    if len(social_accounts) == 1 and not user.has_usable_password():
        variables['last_account'] = True
    for social_account in social_accounts:
        if social_account.get_provider_display() == 'Facebook':
            variables['facebook_added'] = True
            variables['facebook_id'] = social_account.id
        if social_account.get_provider_display() == 'Google':
            variables['google_added'] = True
            variables['google_id'] = social_account.id
        if social_account.get_provider_display() == 'Twitter':
            variables['twitter_added'] = True
            variables['twitter_id'] = social_account.id
    if 'unlink' in request.GET:
        return render(request, 'profilesystem/unlinksocial.html', context=variables)
    if 'link' in request.GET:
        return render(request, 'profilesystem/linksocial.html', context=variables)
    return render(request, 'profilesystem/socialaccount.html', context=variables)


@login_required
def document_page(request):
    variables = {}
    if 'q' in request.GET:
        query = request.GET.get('q')
        documents = UserDocuments.objects.filter(user=request.user).filter(document__icontains=query)
    else:
        documents = UserDocuments.objects.filter(user=request.user)
        variables['show_legal'] = True
    if request.user.profile.avatar:
        variables['show_profile'] = True
    documents_l = []
    image_l = []
    for document in documents:
        a = document.filename().split('.')
        if len(a) > 1:
            if a[1].lower() in IMAGE_EXTENSION:
                image_l.append(document)
            else:
                documents_l.append(document)
        else:
            documents_l.append(document)
    variables['documents'] = documents_l
    variables['images'] = image_l
    return render(request, 'profilesystem/documents.html', context=variables)


@login_required
def delete_document(request):
    if request.method == 'POST':
        doc_id = request.POST.get('id')
        if doc_id == 'p':
            request.user.profile.avatar = ""
            request.user.profile.save()
        else:
            try:
                document = UserDocuments.objects.get(id=doc_id)
                document.delete()
            except ObjectDoesNotExist:
                pass
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()


@login_required
def pinfo_edit_page(request):
    profile = request.user.profile
    uform = UserForm(request, instance=request.user, prefix='userform')
    form = PInfoForm(instance=profile)
    if request.method == 'POST' and request.is_ajax():
        form = PInfoForm(request.POST, instance=profile)
        uform = UserForm(
            request,
            request.POST,
            prefix='userform',
            instance=request.user
        )
        if form.is_valid() and uform.is_valid():
            uform.save()
            form.save()
        else:
            return render(
                request,
                'profilesystem/pinfoform.html',
                {'form': form, 'uform': uform},
                status=500
            )
    return render(request, 'profilesystem/pinfoform.html', {'form': form, 'uform': uform})


@login_required
def phone_edit_page(request):
    try:
        phone = request.user.phone
        form = PhoneForm(instance=phone)
        if request.method == 'POST' and request.is_ajax():
            form = PhoneForm(request.POST, instance=phone)
            if form.is_valid():
                form.save()
            else:
                return render(
                    request,
                    'profilesystem/contactform.html',
                    {'form': form},
                    status=500
                )
    except ObjectDoesNotExist:
        form = PhoneForm()
        if request.method == 'POST' and request.is_ajax():
            form = PhoneForm(request.POST)
            if form.is_valid():
                phone = form.save(commit=False)
                phone.user = request.user
                phone.save()
            else:
                return render(
                    request,
                    'profilesystem/contactform.html',
                    {'form': form},
                    status=500
                )
    return render(request, 'profilesystem/contactform.html', {'form': form})


@login_required
def address_edit_page(request):
    try:
        address = request.user.address
        form = AddressForm(instance=address)
        if request.method == 'POST' and request.is_ajax():
            form = AddressForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
            else:
                return render(
                    request,
                    'profilesystem/addressform.html',
                    {'form': form},
                    status=500
                )
    except ObjectDoesNotExist:
        form = AddressForm()
        if request.method == 'POST' and request.is_ajax():
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
            else:
                return render(
                    request,
                    'profilesystem/addressform.html',
                    {'form': form},
                    status=500
                )
    return render(request, 'profilesystem/addressform.html', {'form': form})


@login_required
def upload_avatar(request):
    if request.POST and request.FILES:
        prof, created = UserProfile.objects.get_or_create(user=request.user)
        prof.avatar = request.FILES['avatarimage']
        prof.save()
        avatar_url = prof.avatar.thumbnail['200x200'].url
    return HttpResponse(avatar_url)


@login_required
def settings(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        pass
    if request.method == 'POST':
        settings_var = request.POST.get('settings_var')
        value = request.POST.get('value')
        if value == 'true':
            try:
                profile = request.user.profile
                setattr(profile, settings_var, True)
                profile.save()
                return HttpResponse('OK')
            except ObjectDoesNotExist:
                return HttpResponse('Error')
        if value == 'false':
            try:
                profile = request.user.profile
                setattr(profile, settings_var, False)
                profile.save()
                return HttpResponse('OK')
            except ObjectDoesNotExist:
                return HttpResponse('Error')
    else:
        return HttpResponseForbidden()


@login_required
def upload_file(request):
    if request.method == 'POST':
        userdoc = UserDocuments(user=request.user)
        userdoc.document = request.FILES['file']
        userdoc.save()
    return HttpResponse('OK')


@login_required
def setuistate(request):
    if request.method == 'POST':
        ui, created = UserUIState.objects.get_or_create(user=request.user)
        ui.state = request.POST.get('uistate')
        ui.save()
    return HttpResponse("OK")


@login_required
def getuistate(request):
    ui, created = UserUIState.objects.get_or_create(user=request.user)
    state = ui.state
    return HttpResponse(state)


@login_required
def set_onlinestate(request):
    current_user = request.user
    if request.method == 'POST':
        cache.set(
            'seen_%s' % current_user.username,
            now(),
            s.USER_LASTSEEN_TIMEOUT
        )
        cache.set(
            '%s_is_online' % current_user.username,
            True,
            s.USER_ONLINE_TIMEOUT
        )
    return HttpResponse("OK")


@login_required
def saveonesignal_id(request):
    if request.method == 'POST':
        onesignal_id = request.POST.get('onesignalid')
        onesignal, created = UserOneSignal.objects.get_or_create(
            user=request.user,
            onesignalid=onesignal_id
        )
        onesignal.save()
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()


@login_required
def send_new_task(request):
    variables = {}
    usercomplete, created = \
        UserCompletionRing.objects.get_or_create(user=request.user)
    completed, completed_list, not_completed, not_completed_list, emailadd = \
        usercomplete.calculate_completed()
    not_verified, not_verified_tasks = usercomplete.calculate_verified()
    task_list = not_completed_list + not_verified_tasks
    if task_list:
        rand = randint(0, len(task_list) - 1)
        ncompleted = task_list[rand]
        variables['ncompleted'] = ncompleted
    return render(
        request,
        'profilesystem/profilecompletiontasks.html',
        context=variables
    )


@login_required
def acknowledge_sys_update(request):
    if request.method == 'POST':
        update_id = int(request.POST.get('id'))
        readsysupdate, created = ReadSysUpdate.objects.get_or_create(
            user=request.user,
            sysupdate=update_id
        )
        readsysupdate.save()
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()
