import json
from datetime import date

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.template import loader

from guardian.shortcuts import assign_perm, remove_perm, get_perms
from guardian.decorators import permission_required_or_403

from groupsystem.models import\
    BasicGroup, GroupNews, GroupPost,\
    PostLikes, PostComment, JoinRequest,\
    GroupEvent, CustomRole, GroupMemberRole,\
    GroupMemberExtraPerm
from groupsystem.forms import\
    CreateGroupForm, CreatePostForm, EditGroupForm,\
    CreateNewsForm, EditPostForm, EditCommentForm,\
    EventForm, NotificationForm, CustomRoleCreateForm,\
    EditRolePermForm, EditExtraPermForm
from groupsystem.tasks import task_create_emailgroup
from notification.utils import create_notification
from publicusers.views import date_handler
from eblast.models import EmailGroup

# Create your views here.


SUPERADMIN_PERMS = [
    ('can_access_admin', _("Can access admin")),
    ('can_read_news', _("Can read news")),
    ('can_create_news', _("Can create news")),
    ('can_update_news', _("Can update news")),
    ('can_delete_news', _("Can delete news")),
    ('can_read_post', _("Can read post")),
    ('can_create_post', _("Can create post")),
    ('can_update_post', _("Can update post")),
    ('can_approve_post', _("Can approve post")),
    ('can_delete_post', _("Can delete post")),
    ('can_read_comment', _("Can read comment")),
    ('can_create_comment', _("Can create comment")),
    ('can_update_comment', _("Can update comment")),
    ('can_approve_comment', _("Can approve comment")),
    ('can_delete_comment', _("Can delete comment")),
    ('can_like_post', _("Can like post")),
    ('can_create_notification', _("Can create notification")),
    ('can_create_invite', _("Can create invite")),
    ('can_add_member', _("Can add member")),
    ('can_remove_member', _("Can remove member")),
    ('can_ban_member', _("Can ban member")),
    ('can_lift_member_ban', _("Can lift member ban")),
    ('can_change_member_role', _("Can change member role")),
    ('can_edit_member_permission', _("Can edit member permission")),
    ('can_read_events', _("Can read events")),
    ('can_create_events', _("Can create events")),
    ('can_update_events', _("Can update events")),
    ('can_delete_events', _("Can delete events")),
    ('can_read_joinrequest', _("Can read join requests")),
    ('can_approve_joinrequest', _("Can approve join requests")),
    ('can_deny_joinrequest', _("Can deny joinrequest")),
    ('can_edit_group_profile', _("Can edit group profile")),
    ('can_read_role', _("Can read role")),
    ('can_read_custom_role', _("Can read custom role")),
    ('can_update_custom_role', _("Can update custom role")),
    ('can_create_custom_role', _("Can create custom role")),
]

ADMIN_PERMS = [
    ('can_access_admin', _("Can access admin")),
    ('can_read_news', _("Can read news")),
    ('can_create_news', _("Can create news")),
    ('can_update_news', _("Can update news")),
    ('can_delete_news', _("Can delete news")),
    ('can_read_post', _("Can read post")),
    ('can_create_post', _("Can create post")),
    ('can_update_post', _("Can update post")),
    ('can_approve_post', _("Can approve post")),
    ('can_delete_post', _("Can delete post")),
    ('can_read_comment', _("Can read comment")),
    ('can_create_comment', _("Can create comment")),
    ('can_update_comment', _("Can update comment")),
    ('can_approve_comment', _("Can approve comment")),
    ('can_delete_comment', _("Can delete comment")),
    ('can_like_post', _("Can like post")),
    ('can_create_invite', _("Can create invite")),
    ('can_add_member', _("Can add member")),
    ('can_remove_member', _("Can remove member")),
    ('can_ban_member', _("Can ban member")),
    ('can_lift_member_ban', _("Can lift member ban")),
    ('can_change_member_role', _("Can change member role")),
    ('can_edit_member_permission', _("Can edit member permission")),
    ('can_read_events', _("Can read events")),
    ('can_create_events', _("Can create events")),
    ('can_update_events', _("Can update events")),
    ('can_delete_events', _("Can delete events")),
    ('can_read_joinrequest', _("Can read join requests")),
    ('can_approve_joinrequest', _("Can approve join requests")),
    ('can_deny_joinrequest', _("Can deny joinrequest")),
]

MODERATOR_PERMS = [
    ('can_access_admin', _("Can access admin")),
    ('can_read_news', _("Can read news")),
    ('can_read_post', _("Can read post")),
    ('can_create_post', _("Can create post")),
    ('can_update_post', _("Can update post")),
    ('can_approve_post', _("Can approve post")),
    ('can_delete_post', _("Can delete post")),
    ('can_read_comment', _("Can read comment")),
    ('can_create_comment', _("Can create comment")),
    ('can_update_comment', _("Can update comment")),
    ('can_approve_comment', _("Can approve comment")),
    ('can_delete_comment', _("Can delete comment")),
    ('can_like_post', _("Can like post")),
    ('can_create_invite', _("Can create invite")),
    ('can_read_events', _("Can read events")),
]

MEMBER_PERMS = [
    ('can_read_news', _("Can read news")),
    ('can_read_post', _("Can read post")),
    ('can_create_post', _("Can create post")),
    ('can_read_comment', _("Can read comment")),
    ('can_create_comment', _("Can create comment")),
    ('can_like_post', _("Can like post")),
    ('can_create_invite', _("Can create invite")),
    ('can_read_events', _("Can read events")),
]

SUBSCRIBER_PERMS = [
    ('can_read_news', _("Can read news")),
]


@login_required
def all_group_page(request):
    query_set = BasicGroup.objects.all()
    if 'qgroup' in request.GET:
        group_name = request.GET.get('qgroup')
        query_set = query_set.filter(name__istartswith=group_name)
    paginator = Paginator(query_set, 10)  # group the users by 10
    page = request.GET.get('page')  # get page no
    try:
        all_groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integet, deliver first page
        all_groups = paginator.page(1)
    except EmptyPage:
        all_groups = paginator.page(paginator.num_pages)
    if 'qgroup' in request.GET:
        return render(
            request,
            'groupsystem/all_group_results.html',
            {
                'all_groups': all_groups
            }
        )
    return render(
        request,
        'groupsystem/all_group.html',
        {
            'all_groups': all_groups,
            'form': CreateGroupForm()
        }
    )


@login_required
def joined_group_page(request):
    query_set = request.user.joined_group.all()
    if 'qgroup' in request.GET:
        group_name = request.GET.get('qgroup')
        query_set = query_set.filter(name__istartswith=group_name)
    paginator = Paginator(query_set, 10)  # group the users by 10
    page = request.GET.get('page')  # get page no
    try:
        joined_groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integet, deliver first page
        joined_groups = paginator.page(1)
    except EmptyPage:
        joined_groups = paginator.page(paginator.num_pages)
    if 'qgroup' in request.GET:
        return render(
            request,
            'groupsystem/joined_group_results.html',
            {
                'joined_groups': joined_groups
            }
        )
    return render(
        request,
        'groupsystem/joined_group.html',
        {
            'joined_groups': joined_groups,
            'form': CreateGroupForm(),
        }
    )


@login_required
def subscribed_group_page(request):
    query_set = request.user.subscribed_group.all()
    if 'qgroup' in request.GET:
        group_name = request.GET.get('qgroup')
        query_set = query_set.filter(name__istartswith=group_name)
    paginator = Paginator(query_set, 10)  # group the users by 10
    page = request.GET.get('page')  # get page no
    try:
        user_groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integet, deliver first page
        user_groups = paginator.page(1)
    except EmptyPage:
        user_groups = paginator.page(paginator.num_pages)
    if 'qgroup' in request.GET:
        return render(
            request,
            'groupsystem/subscribed_group_results.html',
            {
                'user_groups': user_groups
            }
        )
    return render(
        request,
        'groupsystem/subscribed_group.html',
        {
            'user_groups': user_groups,
            'form': CreateGroupForm()
        }
    )


@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            basicgroup = form.save(commit=False)
            logo = open('media/group_logo/default.png', 'r')
            basicgroup.logo = File(logo)
            basicgroup.save()
            logo.close()
            basicgroup.super_admins.add(request.user)
            basicgroup.members.add(request.user)
            basicgroup.subscribers.add(request.user)
            super_admin_group = Group.objects.create(
                name='%s_superadmin' % basicgroup.id
            )
            admin_group = Group.objects.create(
                name='%s_admin' % basicgroup.id
            )
            moderator_group = Group.objects.create(
                name='%s_moderator' % basicgroup.id
            )
            member_group = Group.objects.create(
                name='%s_member' % basicgroup.id
            )
            subscriber_group = Group.objects.create(
                name='%s_subscriber' % basicgroup.id
            )
            for perm in SUPERADMIN_PERMS:
                assign_perm(perm[0], super_admin_group, basicgroup)
            for perm in ADMIN_PERMS:
                assign_perm(perm[0], admin_group, basicgroup)
            for perm in MODERATOR_PERMS:
                assign_perm(perm[0], moderator_group, basicgroup)
            for perm in MEMBER_PERMS:
                assign_perm(perm[0], member_group, basicgroup)
            for perm in SUBSCRIBER_PERMS:
                assign_perm(perm[0], subscriber_group, basicgroup)
            request.user.groups.add(super_admin_group)
            groupmemberrole = GroupMemberRole(basic_group=basicgroup)
            groupmemberrole.user = request.user
            groupmemberrole.role_name = 'superadmin'
            groupmemberrole.save()
            extraperm = GroupMemberExtraPerm(basic_group=basicgroup)
            extraperm.user = request.user
            for perm in SUPERADMIN_PERMS:
                setattr(extraperm, perm[0], True)
            extraperm.save()
            task_create_emailgroup.delay(basicgroup)
            return render(
                request,
                'groupsystem/creategroupsuccess.html',
                {
                    'group': basicgroup
                }
            )
        else:
            return render(
                request,
                'groupsystem/creategroupform.html',
                {'form': form},
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
def basic_group_details(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    notifications = basicgroup.notifications.all().order_by('-created_on')
    if notifications:
        notifications = notifications[0]
    try:
        joinrequest_sent = JoinRequest.objects.get(
            basic_group=basicgroup,
            user=request.user
        )
    except ObjectDoesNotExist:
        joinrequest_sent = None
    if request.user in basicgroup.super_admins.all():
        if basicgroup.super_admins.count() == 1:
            onlysuperadmin = True
        else:
            onlysuperadmin = False
    else:
        onlysuperadmin = False
    if request.method == 'POST':
        req_type = request.POST.get('type')
        if req_type == 'join':
            if request.user not in basicgroup.banned_members.all():
                joinrequest, created = JoinRequest.objects.get_or_create(
                    basic_group=basicgroup,
                    user=request.user
                )
                if created:
                    admins = basicgroup.super_admins.all() | basicgroup.admins.all()
                    for admin in admins:
                        create_notification(
                            user=admin,
                            ntype=12,
                            sender=request.user.username,
                            sender_id=request.user.id,
                            group_name=basicgroup.name,
                            group_id=basicgroup.id
                        )
                    data = json.dumps(
                        {
                            'id': joinrequest.id,
                            'msg': "Request sent"
                        }
                    )
                    mimetype = 'application/json'
                    return HttpResponse(data, mimetype)
                else:
                    return HttpResponse(_("Already requested"))
            else:
                return HttpResponse(_("You're banned from this group"))
        elif req_type == 'subscribe':
            basicgroup.subscribers.add(request.user)
            subscriber_group = Group.objects.get(
                name='%s_subscriber' % basicgroup.id
            )
            request.user.groups.add(subscriber_group)
            return HttpResponse(_("Subscribed"))
        elif req_type == 'unsubscribe':
            basicgroup.subscribers.remove(request.user)
            subscriber_group = Group.objects.get(
                name='%s_subscriber' % basicgroup.id
            )
            request.user.groups.remove(subscriber_group)
            return HttpResponse(_("Unsubscribed"))
        elif req_type == 'cancel':
            joinrequest = JoinRequest.objects.get(
                id=request.POST.get('request_id')
            )
            joinrequest.delete()
            return HttpResponse(_("Request Canceled"))
        elif req_type == 'leave':
            if request.POST.get('request_id') != '':
                joinrequest = JoinRequest.objects.get(
                    id=request.POST.get('request_id')
                    )
                joinrequest.delete()
            basicgroup.members.remove(request.user)
            basicgroup.super_admins.remove(request.user)
            basicgroup.admins.remove(request.user)
            basicgroup.moderators.remove(request.user)
            perm_groups = request.user.groups.filter(
                name__istartswith=basicgroup.id
            )
            for perm_group in perm_groups:
                request.user.groups.remove(perm_group)
            groupmemberrole = GroupMemberRole.objects.get(
                basic_group=basicgroup,
                user=request.user
            )
            groupmemberrole.delete()
            extraperm = GroupMemberExtraPerm.objects.get(
                basic_group=basicgroup,
                user=request.user
            )
            for perm in SUPERADMIN_PERMS:
                if extraperm.__getattribute__(perm[0]):
                    remove_perm(perm[0], request.user, basicgroup)
            extraperm.delete()
            emailgroup = basicgroup.emailgroup
            emailgroup.users.remove(request.user)
            return HttpResponse(_("Leaved Group"))
        else:
            return HttpResponseForbidden()
    return render(
        request,
        'groupsystem/groupdetails.html',
        {
            'group': basicgroup,
            'group_notification': notifications if notifications else None,
            'joinrequest_sent': joinrequest_sent,
            'onlysuperadmin': onlysuperadmin,
            'extended_sidebar': True,
            'user_in_group': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_read_news', (BasicGroup, 'id', 'group_id'))
def news_details(request, news_id, group_id):
    try:
        news = GroupNews.objects.get(id=news_id)
        news_title = news.title
        news_content = news.news
        news_dict = {
            'title': news_title,
            'content': news_content
        }
        data = json.dumps(news_dict)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


@login_required
@permission_required_or_403('can_read_events', (BasicGroup, 'id', 'group_id'))
def group_events_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    events = basicgroup.events.all()
    return render(
        request,
        'groupsystem/events.html',
        {
            'group': basicgroup,
            'events': events,
            'extended_sidebar': True,
            'user_in_group': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_read_post', (BasicGroup, 'id', 'group_id'))
def group_posts(request, group_id):
    user_is_admin = False
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    if request.user in basicgroup.super_admins.all() or request.user in\
            basicgroup.admins.all() or request.user in\
            basicgroup.moderators.all():
            user_is_admin = True
    if user_is_admin:
        posts = basicgroup.posts.all().order_by('-created_on')
    else:
        posts = basicgroup.posts.filter(approved=True).order_by('-created_on')
    return render(
        request,
        'groupsystem/posts.html',
        {
            'group': basicgroup,
            'posts': posts,
            'form': CreatePostForm(),
            'user_is_admin': user_is_admin,
            'extended_sidebar': True,
            'user_in_group': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_create_post', (BasicGroup, 'id', 'group_id'))
def create_member_post(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.basic_group = basicgroup
            post.creator = request.user
            post.admin_created = False
            if basicgroup.auto_approve_post:
                post.approved = True
            post.save()
            if basicgroup.auto_approve_post:
                new_date = False
                template = loader.get_template('groupsystem/singlepost.html')
                posts = basicgroup.posts.filter(approved=True,
                                                created_on__gte=date.today())
                if not posts:
                    new_date = True
                contexts = {'group': basicgroup,
                            'post': post, 'new_date': new_date,
                            'request': request}
                post_html = template.render(contexts)
                response_data = {
                    'response_type': 'html',
                    'new_date': new_date,
                    'response': post_html
                }
                data = json.dumps(response_data)
                content_type = 'application/json'
                return HttpResponse(data, content_type)
            else:
                return HttpResponse(
                    _("Post will be shown once admin/moderator approves")
                )
        else:
            return render(
                request,
                'groupsystem/createpost.html',
                {'form': form, 'group': basicgroup},
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
def edit_post(request, group_id, post_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    post = GroupPost.objects.get(id=post_id)
    form = CreatePostForm(instance=post)
    if request.user == post.creator or request.user.has_perm(
        'can_update_post', basicgroup):
        if request.method == 'POST':
            form = CreatePostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                new_date = False
                template = loader.get_template('groupsystem/singlepost.html')
                posts = basicgroup.posts.filter(approved=True,
                                                created_on__gte=date.today())
                if not posts:
                    new_date = True
                contexts = {'group': basicgroup,
                            'post': post, 'new_date': new_date,
                            'request': request}
                post_html = template.render(contexts)
                response_data = {
                    'response_type': 'html',
                    'new_date': new_date,
                    'response': post_html
                }
                data = json.dumps(response_data)
                content_type = 'application/json'
                return HttpResponse(data, content_type)
            else:
                return render(
                    request,
                    'groupsystem/editpost.html',
                    {
                        'form': form,
                        'group': basicgroup,
                        'post': post
                    },
                    status=500
                )
        return render(
            request,
            'groupsystem/editpost.html',
            {
                'form': form,
                'group': basicgroup,
                'post': post
            }
        )
    else:
        return HttpResponseForbidden()


@require_POST
@login_required
def delete_post(request, group_id, post_id):
    group = BasicGroup.objects.get(id=group_id)
    post = GroupPost.objects.get(id=post_id)
    if request.user == post.creator:
        post.delete()
        return HttpResponse(status=200)
    elif request.user.has_perm('can_delete_post', group):
        post.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden()


@login_required
@permission_required_or_403('can_like_post', (BasicGroup, 'id', 'group_id'))
def like_post(request, post_id, group_id):
    post = GroupPost.objects.get(id=post_id)
    if request.method == 'POST':
        like = PostLikes(liker=request.user)
        like.post = post
        like.save()
        post_social = {
            'likes': post.likes.count(),
            'comments': post.comments.count()
        }
        data = json.dumps(post_social)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        return HttpResponseForbidden()


@login_required
@permission_required_or_403('can_create_comment', (BasicGroup, 'id', 'group_id'))
def comment_post(request, group_id, post_id):
    group = BasicGroup.objects.get(id=group_id)
    post = GroupPost.objects.get(id=post_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        postcomment = PostComment(commentor=request.user)
        postcomment.post = post
        postcomment.comment = comment
        postcomment.basic_group = group
        if group.auto_approve_comment:
            postcomment.approved = True
        postcomment.save()
        if group.auto_approve_comment:
            template = loader.get_template('groupsystem/singlecomment.html')
            contexts = {'comment': postcomment, 'group': group,
                        'request': request}
            comment_html = template.render(contexts)
            response_data = {
                'response_type': 'html',
                'response': comment_html
            }
            data = json.dumps(response_data)
            content_type = 'application/json'
            return HttpResponse(data, content_type)
        else:
            return HttpResponse(
                _("Thank you for commenting your comment will show once a admin/moderator approves")
            )
    else:
        return HttpResponseForbidden()


@require_POST
@login_required
def delete_comment(request, group_id, comment_id):
    group = BasicGroup.objects.get(id=group_id)
    comment = PostComment.objects.get(id=comment_id)
    if request.user == comment.commentor:
        comment.delete()
        return HttpResponse(status=200)
    elif request.user.has_perm('can_delete_comment', group):
        comment.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden()


@login_required
# @permission_required_or_403('can_edit_group_profile', (BasicGroup, 'id', 'group_id'))
def group_admin_settings_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    form = EditGroupForm(basicgroup=basicgroup, instance=basicgroup)
    notificationform = NotificationForm()
    if request.method == 'POST':
        form = EditGroupForm(request.POST, request.FILES,
                             basicgroup=basicgroup, instance=basicgroup)
        if form.is_valid():
            form.save()
    return render(
        request,
        'groupsystem/adminsettings.html',
        {
            'group': basicgroup,
            'form': form,
            'notificationform': notificationform,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@require_POST
@login_required
def group_admin_settings_toggle(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.user.has_perm('can_edit_group_profile', basicgroup):
        if 'post_toggle' in request.POST:
            post_toggle = request.POST.get('post_toggle')
            if post_toggle == 'on':
                basicgroup.auto_approve_post = True
            if post_toggle == 'off':
                basicgroup.auto_approve_post = False
            basicgroup.save()
            return HttpResponse(status=200)
        if 'comment_toggle' in request.POST:
            comment_toggle = request.POST.get('comment_toggle')
            if comment_toggle == 'on':
                basicgroup.auto_approve_comment = True
            if comment_toggle == 'off':
                basicgroup.auto_approve_comment = False
            basicgroup.save()
            return HttpResponse(status=200)
    else:
        return HttpResponseForbidden(
            _('You don\'t have permissions to edit settings')
        )


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def group_admin_news_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    news = basicgroup.news.all()
    form = CreateNewsForm()
    if request.method == 'POST':
        if request.user.has_perm('can_create_news', basicgroup):
            form = CreateNewsForm(request.POST)
            if form.is_valid():
                news = form.save(commit=False)
                news.creator = request.user
                news.basic_group = basicgroup
                news.save()
        else:
            return HttpResponseForbidden(_("You don't have permission to create news"))
    return render(
        request,
        'groupsystem/adminnews.html',
        {
            'group': basicgroup,
            'news': news,
            'form': form,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_update_news', (BasicGroup, 'id', 'group_id'))
def edit_news(request, group_id):
    news_id = request.GET.get('news_id')
    news = GroupNews.objects.get(id=news_id)
    basicgroup = BasicGroup.objects.get(id=group_id)
    form = CreateNewsForm(instance=news)
    if request.method == 'POST':
        form = CreateNewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponse("OK")
        else:
            return render(
                request,
                'groupsystem/editnews.html',
                {
                    'form': form,
                    'news': news,
                    'group': basicgroup
                },
                status=500
            )
    return render(
        request,
        'groupsystem/editnews.html',
        {
            'form': form,
            'news': news,
            'group': basicgroup
        }
    )


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def groupadmin_admin_post_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    posts = basicgroup.posts.filter(admin_created=True)
    return render(
        request,
        'groupsystem/postsadmin.html',
        {
            'group': basicgroup,
            'posts': posts,
            'adminpost': True,
            'form': CreatePostForm(),
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def groupadmin_member_post_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    posts = basicgroup.posts.filter(admin_created=False)
    return render(
        request,
        'groupsystem/postsadmin.html',
        {
            'group': basicgroup,
            'posts': posts,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
def approve_post(request, group_id):
    if request.method == 'POST':
        basicgroup = BasicGroup.objects.get(id=group_id)
        if request.user.has_perm('can_approve_post', basicgroup):
            post_id = request.POST.get('post_id')
            post = GroupPost.objects.get(id=post_id)
            post.approved = True
            post.approved_by = request.user
            post.save()
            return HttpResponse()
        else:
            return HttpResponseForbidden(
                _("You dont have permissions to approve post")
            )
    else:
        return HttpResponseForbidden()


@login_required
@permission_required_or_403('can_create_post', (BasicGroup, 'id', 'group_id'))
def create_admin_post(request, group_id):
    user_is_admin = False
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.user in basicgroup.super_admins.all() or request.user in\
            basicgroup.admins.all() or request.user in\
            basicgroup.moderators.all():
            user_is_admin = True
    if request.method == 'POST' and user_is_admin:
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.basic_group = basicgroup
            post.creator = request.user
            post.admin_created = True
            post.approved = True
            post.save()
            new_date = False
            template = loader.get_template('groupsystem/singlepost.html')
            posts = basicgroup.posts.filter(approved=True,
                                            created_on__gte=date.today())
            if not posts:
                new_date = True
            contexts = {'group': basicgroup,
                        'post': post, 'new_date': new_date,
                        'request': request}
            post_html = template.render(contexts)
            response_data = {
                'response_type': 'html',
                'new_date': new_date,
                'response': post_html
            }
            data = json.dumps(response_data)
            content_type = 'application/json'
            return HttpResponse(data, content_type)
        else:
            return render(
                request,
                'groupsystem/createpost.html',
                {'form': form, 'group': basicgroup},
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def notapproved_comment_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    comments = basicgroup.postcomments.filter(approved=False)
    return render(
        request,
        'groupsystem/commentadmin.html',
        {
            'group': basicgroup,
            'comments': comments,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def approved_comment_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    comments = basicgroup.postcomments.filter(approved=True)
    return render(
        request,
        'groupsystem/commentadmin.html',
        {
            'group': basicgroup,
            'comments': comments,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@require_POST
@login_required
def edit_comment(request, group_id, comment_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    comment = PostComment.objects.get(id=comment_id)
    if request.user == comment.commentor or request.user.has_perm(
        'can_update_comment', basicgroup):
        comment.comment = request.POST.get('comment')
        comment.save()
        return render(
            request,
            'groupsystem/singlecomment.html',
            {
                'comment': comment,
                'group': basicgroup
            }
        )
    else:
        return HttpResponseForbidden()


@login_required
def approve_comment(request, group_id):
    if request.method == 'POST':
        basicgroup = BasicGroup.objects.get(id=group_id)
        if request.user.has_perm('can_approve_comment', basicgroup):
            comment_id = request.POST.get('comment_id')
            comment = PostComment.objects.get(id=comment_id)
            comment.approved = True
            comment.approved_by = request.user
            comment.save()
            return HttpResponse()
        else:
            return HttpResponseForbidden(
                _("You dont have permissions to approve comment")
            )
    else:
        return HttpResponseForbidden()



@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def group_member_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    memberroles = basicgroup.memberrole.all()
    if request.method == 'POST':
        req_type = request.POST.get('req_type')
        if req_type == 'addmembers':
            usernames = request.POST.get('usernames').split(',')
            if request.user.has_perm('can_add_member', basicgroup):
                for username in usernames:
                    try:
                        user = User.objects.get(username=username)
                        basicgroup.members.add(user)
                        member_group = Group.objects.get(
                            name='%s_member' % basicgroup.id
                        )
                        user.groups.add(member_group)
                        groupmemberrole, created = GroupMemberRole.objects.get_or_create(
                            basic_group=basicgroup,
                            user=user
                        )
                        groupmemberrole.user = user
                        groupmemberrole.role_name = 'member'
                        groupmemberrole.save()
                        extraperm = GroupMemberExtraPerm(basic_group=basicgroup)
                        extraperm.user = user
                        for perm in MEMBER_PERMS:
                            setattr(extraperm, perm[0], True)
                        extraperm.save()
                        emailgroup = basicgroup.emailgroup
                        emailgroup.users.add(user)
                    except ObjectDoesNotExist:
                        pass
                return HttpResponse("OK")
            else:
                return HttpResponseForbidden(
                    _("You don't have permission to add memeber")
                )
        elif req_type == 'removemember':
            if request.user.has_perm('can_remove_member', basicgroup):
                username = request.POST.get('username')
                user = User.objects.get(username=username)
                basicgroup.members.remove(user)
                basicgroup.super_admins.remove(user)
                basicgroup.admins.remove(user)
                basicgroup.moderators.remove(user)
                try:
                    joinrequest = basicgroup.joinrequest.get(user=user)
                    joinrequest.delete()
                except ObjectDoesNotExist:
                    pass
                usergroups = user.groups.filter(name__istartswith=basicgroup.id)
                for usergroup in usergroups:
                    user.groups.remove(usergroup)
                groupmemberrole = GroupMemberRole.objects.get(
                    basic_group=basicgroup,
                    user=user
                )
                groupmemberrole.delete()
                extraperm = GroupMemberExtraPerm.objects.get(
                    basic_group=basicgroup,
                    user=user
                )
                for perm in SUPERADMIN_PERMS:
                    if extraperm.__getattribute__(perm[0]):
                        remove_perm(perm[0], user, basicgroup)
                extraperm.delete()
                emailgroup = basicgroup.emailgroup
                emailgroup.users.remove(user)
                data = json.dumps({'id': user.id})
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            else:
                return HttpResponseForbidden(
                    _("You dont have permission to remove member")
                )
        elif req_type == 'banmember':
            if request.user.has_perm('can_ban_member', basicgroup):
                username = request.POST.get('username')
                user = User.objects.get(username=username)
                if user in basicgroup.members.all():
                    basicgroup.members.remove(user)
                basicgroup.super_admins.remove(user)
                basicgroup.admins.remove(user)
                basicgroup.moderators.remove(user)
                basicgroup.banned_members.add(user)
                try:
                    joinrequest = basicgroup.joinrequest.get(user=user)
                    joinrequest.delete()
                except ObjectDoesNotExist:
                    pass
                usergroups = user.groups.filter(name__istartswith=basicgroup.id)
                for usergroup in usergroups:
                    user.groups.remove(usergroup)
                groupmemberrole = GroupMemberRole.objects.get(
                    basic_group=basicgroup,
                    user=user
                )
                groupmemberrole.delete()
                extraperm = GroupMemberExtraPerm.objects.get(
                    basic_group=basicgroup,
                    user=user
                )
                for perm in SUPERADMIN_PERMS:
                    if extraperm.__getattribute__(perm[0]):
                        remove_perm(perm[0], user, basicgroup)
                extraperm.delete()
                emailgroup = basicgroup.emailgroup
                emailgroup.users.remove(user)
                data = json.dumps({'id': user.id})
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            else:
                return HttpResponseForbidden(
                    _("You dont have permission to ban member")
                )
        elif req_type == 'changerole':
            if request.user.has_perm('can_change_member_role', basicgroup):
                username = request.POST.get('username')
                role_name = request.POST.get('role_name')
                user = User.objects.get(username=username)
                groupmemberrole, created = GroupMemberRole.objects.get_or_create(
                    basic_group=basicgroup,
                    user=user
                )
                groupmemberrole.role_name = role_name
                groupmemberrole.save()
                usergroups = user.groups.filter(name__istartswith=basicgroup.id)
                for usergroup in usergroups:
                    user.groups.remove(usergroup)
                permission_group = Group.objects.get(name='%s_%s' % (basicgroup.id, role_name))
                user.groups.add(permission_group)
                extraperm = GroupMemberExtraPerm.objects.get(
                    basic_group=basicgroup,
                    user=user
                )
                for perm in SUPERADMIN_PERMS:
                    if perm[0] in get_perms(permission_group, basicgroup):
                        setattr(extraperm, perm[0], True)
                    else:
                        setattr(extraperm, perm[0], False)
                        remove_perm(perm[0], user, basicgroup)
                extraperm.save()
                if role_name == 'superadmin':
                    basicgroup.super_admins.add(user)
                else:
                    basicgroup.super_admins.remove(user)
                if role_name == 'admin':
                    basicgroup.admins.add(user)
                else:
                    basicgroup.admins.remove(user)
                if role_name == 'moderator':
                    basicgroup.moderators.add(user)
                else:
                    basicgroup.moderators.remove(user)
                data = json.dumps(
                    {
                        'id': user.id,
                        'role_name': role_name
                    }
                )
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            else:
                return HttpResponseForbidden(
                    _("You don't have permissions to change member role")
                )
        else:
            return HttpResponseForbidden()
    return render(
        request,
        'groupsystem/members.html',
        {
            'group': basicgroup,
            'memberroles': memberroles,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_lift_member_ban', (BasicGroup, 'id', 'group_id'))
def group_banned_members_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        basicgroup.banned_members.remove(user)
        data = json.dumps({'id': user.id})
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    return render(
        request,
        'groupsystem/bannedmembers.html',
        {
            'group': basicgroup,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
def users_autocomplete(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__istartswith=q)[:20]
        filteredusers = []
        results = []
        for user in users:
            if user not in basicgroup.members.all() and user not in basicgroup.banned_members.all():
                filteredusers.append(user)
        for user in filteredusers:
            user_json = {}
            if user.username == request.user.username:
                pass
            else:
                user_json['value'] = user.username
                results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def joinrequest_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    joinrequests = basicgroup.joinrequest.filter(approved=False)
    if request.method == 'POST':
        req_type = request.POST.get('req_type')
        if req_type == 'approve':
            if request.user.has_perm('can_approve_joinrequest', basicgroup):
                request_id = request.POST.get('request_id')
                joinrequest = JoinRequest.objects.get(id=request_id)
                user = joinrequest.user
                basicgroup.members.add(user)
                joinrequest.approved = True
                joinrequest.save()
                member_group = Group.objects.get(
                    name='%s_member' % basicgroup.id
                )
                user.groups.add(member_group)
                groupmemberrole, created = GroupMemberRole.objects.get_or_create(
                    basic_group=basicgroup,
                    user=user
                )
                groupmemberrole.user = user
                groupmemberrole.role_name = 'member'
                groupmemberrole.save()
                extraperm = GroupMemberExtraPerm(basic_group=basicgroup)
                extraperm.user = user
                for perm in MEMBER_PERMS:
                    setattr(extraperm, perm[0], True)
                extraperm.save()
                emailgroup = basicgroup.emailgroup
                emailgroup.users.add(user)
                joinrequest_id = {'id': joinrequest.id}
                data = json.dumps(joinrequest_id)
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            else:
                return HttpResponseForbidden(
                    _("You don't have permission to approve request")
                )
        elif req_type == 'deny':
            if request.user.has_perm('can_deny_joinrequest', basicgroup):
                request_id = request.POST.get('request_id')
                joinrequest = JoinRequest.objects.get(id=request_id)
                joinrequest_id = {'id': joinrequest.id}
                data = json.dumps(joinrequest_id)
                mimetype = 'application/json'
                joinrequest.delete()
                return HttpResponse(data, mimetype)
            else:
                return HttpResponseForbidden(
                    _("You don't have permission to deny request")
                )
        else:
            return HttpResponseForbidden()
    return render(
        request,
        'groupsystem/joinrequests.html',
        {
            'group': basicgroup,
            'joinrequests': joinrequests,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_create_invite', (BasicGroup, 'id', 'group_id'))
def invite_user(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.method == 'POST':
        receiver = request.POST.get("receivers")
        usernames = receiver.split(',')
        for username in usernames:
            try:
                user = User.objects.get(username=username)
                create_notification(
                    user=user,
                    ntype=11,
                    sender=request.user.username,
                    sender_id=request.user.id,
                    group_name=basicgroup.name,
                    group_id=basicgroup.id
                )
            except ObjectDoesNotExist:
                pass
    return HttpResponse(_("Users invited"))


@login_required
@permission_required_or_403('can_create_events', (BasicGroup, 'id', 'group_id'))
def group_events_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    events = basicgroup.events.all()
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            if event_id:
                event = GroupEvent.objects.get(id=event_id)
            else:
                event = GroupEvent(basic_group=basicgroup)
            event.creator = request.user
            event.title = form.cleaned_data['title']
            event.start = form.cleaned_data['start_date']
            event.end = form.cleaned_data['end_date']
            event.background_color = form.cleaned_data['color']
            event.border_color = form.cleaned_data['color']
            event.save()
            event_dict = {
                'id': event.id,
                'title': event.title,
                'start': event.start,
                'end': event.end,
                'backgroundColor': event.background_color,
                'borderColor': event.border_color
            }
            data = json.dumps(event_dict, default=date_handler)
            mimetype = 'application/json'
            return HttpResponse(data, mimetype)
        else:
            return render(
                request,
                'groupsystem/eventform.html',
                {
                    'form': form,
                    'group': basicgroup
                },
                status=500
            )
    return render(
        request,
        'groupsystem/eventsadmin.html',
        {
            'group': basicgroup,
            'events': events,
            'form': form,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_create_notification', (BasicGroup, 'id', 'group_id'))
def create_notification_admin(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    if request.method == 'POST':
        notificationform = NotificationForm(request.POST)
        if notificationform.is_valid():
            notification = notificationform.save(commit=False)
            notification.basic_group = basicgroup
            notification.creator = request.user
            notification.save()
            return HttpResponse("OK")
        else:
            return render(
                request,
                'groupsystem/createnotificationform.html',
                {
                    'group': basicgroup,
                    'notificationform': notificationform
                },
                status=500
            )
    else:
        return HttpResponseForbidden()


@login_required
@permission_required_or_403('can_access_admin', (BasicGroup, 'id', 'group_id'))
def group_dashboard_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    pendingpost = GroupPost.objects.filter(
        basic_group=basicgroup
    ).filter(approved=False).count()
    pendingcomment = PostComment.objects.filter(
        basic_group=basicgroup
    ).filter(approved=False).count()
    joinrequests = JoinRequest.objects.filter(
        basic_group=basicgroup
    ).filter(approved=False).count()
    return render(
        request,
        'groupsystem/admindashboard.html',
        {
            'group': basicgroup,
            'pendingpost': pendingpost,
            'pendingcomment': pendingcomment,
            'joinrequests': joinrequests,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_read_role', (BasicGroup, 'id', 'group_id'))
def group_default_role_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    default_roles = basicgroup.default_roles.split(';')
    if 'role_details' in request.GET:
        role = request.GET.get('role_details')
        if role == 'superadmin':
            permissions = []
            for perm in SUPERADMIN_PERMS:
                permissions.append(perm[1])
            return render(
                request,
                'groupsystem/roledetails.html',
                {
                    'permissions': permissions
                }
            )
        elif role == 'admin':
            permissions = []
            for perm in ADMIN_PERMS:
                permissions.append(perm[1])
            return render(
                request,
                'groupsystem/roledetails.html',
                {
                    'permissions': permissions
                }
            )
        elif role == 'moderator':
            permissions = []
            for perm in MODERATOR_PERMS:
                permissions.append(perm[1])
            return render(
                request,
                'groupsystem/roledetails.html',
                {
                    'permissions': permissions
                }
            )
        elif role == 'member':
            permissions = []
            for perm in MEMBER_PERMS:
                permissions.append(perm[1])
            return render(
                request,
                'groupsystem/roledetails.html',
                {
                    'permissions': permissions
                }
            )
        elif role == 'subscriber':
            permissions = []
            for perm in SUBSCRIBER_PERMS:
                permissions.append(perm[1])
            return render(
                request,
                'groupsystem/roledetails.html',
                {
                    'permissions': permissions
                }
            )
        else:
            return render(
                request,
                'groupsystem/roledetails.html',
            )
    return render(
        request,
        'groupsystem/defaultroles.html',
        {
            'group': basicgroup,
            'defaultroles': default_roles,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_read_custom_role', (BasicGroup, 'id', 'group_id'))
def group_custom_role_admin_page(request, group_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    request.session['basicgroup'] = basicgroup.id
    customroles = basicgroup.customrole.all()
    form = CustomRoleCreateForm()
    if request.method == 'POST':
        form = CustomRoleCreateForm(request.POST, group_id=basicgroup.id)
        if request.user.has_perm('can_create_custom_role', basicgroup):
            if form.is_valid():
                customrole = form.save(commit=False)
                customrole.basic_group = basicgroup
                customrole.permission_group = '%s_%s' % (basicgroup.id, customrole.custom_role_name)
                customrole.save()
                Group.objects.create(name=customrole.permission_group)
                return HttpResponse(_("Role created, reload page to edit permissions"))
            else:
                return render(
                    request,
                    'groupsystem/customroleform.html',
                    {
                        'form': form,
                        'group': basicgroup
                    },
                    status=500
                )
        else:
            return HttpResponseForbidden(
                _("You don't have permission to create custom role")
            )
    return render(
        request,
        'groupsystem/customroles.html',
        {
            'group': basicgroup,
            'form': form,
            'customroles': customroles,
            'extended_sidebar': True,
            'user_in_group_admin': True,
            'user_has_admin_access': request.user.has_perm(
                'can_access_admin', basicgroup
            )
        }
    )


@login_required
@permission_required_or_403('can_update_custom_role', (BasicGroup, 'id', 'group_id'))
def edit_permissions(request, group_id, custom_role_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    customrole = CustomRole.objects.get(id=custom_role_id)
    form = EditRolePermForm(instance=customrole)
    if request.method == 'POST':
        form = EditRolePermForm(request.POST, instance=customrole)
        if form.is_valid():
            form.save()
            perm_group = Group.objects.get(name=customrole.permission_group)
            enabled_perms = []
            for perm in SUPERADMIN_PERMS:
                remove_perm(perm[0], perm_group, basicgroup)
                if customrole.__getattribute__(perm[0]):
                    enabled_perms.append(perm[0])
            for perm in enabled_perms:
                assign_perm(perm, perm_group, basicgroup)
            return HttpResponse(_("Role permission changed"))
        else:
            return render(
                request,
                'groupsystem/editcustomrole.html',
                {
                    'group': basicgroup,
                    'customrole': customrole,
                    'form': form
                },
                status=500
            )
    return render(
        request,
        'groupsystem/editcustomrole.html',
        {
            'group': basicgroup,
            'customrole': customrole,
            'form': form
        }
    )


@login_required
@permission_required_or_403('can_edit_member_permission', (BasicGroup, 'id', 'group_id'))
def edit_extra_permissions(request, group_id, user_id):
    basicgroup = BasicGroup.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    extraperm, created = GroupMemberExtraPerm.objects.get_or_create(
        basic_group=basicgroup,
        user=user
    )
    form = EditExtraPermForm(instance=extraperm)
    if request.method == 'POST':
        form = EditExtraPermForm(request.POST, instance=extraperm)
        if form.is_valid():
            form.save()
            extra_perms = []
            for perm in SUPERADMIN_PERMS:
                if extraperm.__getattribute__(perm[0]):
                    assign_perm(perm[0], user, basicgroup)
                else:
                    remove_perm(perm[0], user, basicgroup)
            return HttpResponse(_("User permission changed"))
        else:
            return render(
                request,
                'groupsystem/editextraperm.html',
                {
                    'group': basicgroup,
                    'user': user,
                    'form': form
                },
                status=500
            )
    return render(
        request,
        'groupsystem/editextraperm.html',
        {
            'group': basicgroup,
            'user': user,
            'form': form
        }
    )


@require_POST
@csrf_exempt
def integrate_users(request):
    data = request.POST.get('data')
    for obj in serializers.deserialize('json', data):
        obj.save()
    return HttpResponse(status=200)
