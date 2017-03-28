from django.conf.urls import url
from groupsystem import views


urlpatterns = [
    url(
        r'^groups/$',
        views.all_group_page,
        name='allgroups'
    ),
    url(
        r'^joinedgroups/$',
        views.joined_group_page,
        name='joinedgroups'
    ),
    url(
        r'^subscribedgroups/$',
        views.subscribed_group_page,
        name='subscribedgroups'
    ),
    url(
        r'^creategroup/$',
        views.create_group,
        name='creategroup'
    ),
    url(
        r'^group/(?P<group_id>\d+)/$',
        views.basic_group_details,
        name='groupdetails'
    ),
    url(
        r'^group/(?P<group_id>\d+)/n/(?P<news_id>\d+)/$',
        views.news_details,
        name='newsdetails'
    ),
    url(
        r'^group/(?P<group_id>\d+)/events/$',
        views.group_events_page,
        name='events'
    ),
    url(
        r'^group/(?P<group_id>\d+)/posts/$',
        views.group_posts,
        name='posts'
    ),
    url(
        r'^group/deletepost/(?P<group_id>\d+)/(?P<post_id>\d+)/$',
        views.delete_post,
        name='deletepost'
    ),
    url(
        r'^group/(?P<group_id>\d+)/l/(?P<post_id>\d+)/$',
        views.like_post,
        name='like'
    ),
    url(
        r'^group/c/(?P<group_id>\d+)/(?P<post_id>\d+)/$',
        views.comment_post,
        name='comment'
    ),
    url(
        r'^group/deletecomment/(?P<group_id>\d+)/(?P<comment_id>\d+)/$',
        views.delete_comment,
        name='deletecomment'
    ),
    url(
        r'^group/creatememberpost/(?P<group_id>\d+)/$',
        views.create_member_post,
        name='creatememberpost'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/settings/$',
        views.group_admin_settings_page,
        name='adminsettings'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/news/$',
        views.group_admin_news_page,
        name='adminnews'
    ),
    url(
        r'^group/(?P<group_id>\d+)/editnews/$',
        views.edit_news,
        name='editnews'
    ),
    url(
        r'^group/(?P<group_id>\d+)/grouppostsadmin/$',
        views.groupadmin_admin_post_page,
        name='adminpostsadmin'
    ),
    url(
        r'^group/(?P<group_id>\d+)/grouppostsadmin/membercreated/$',
        views.groupadmin_member_post_page,
        name='memberpostsadmin'
    ),
    url(
        r'^creatadminpost/(?P<group_id>\d+)/$',
        views.create_admin_post,
        name='createadminpost'
    ),
    url(
        r'^editpost/(?P<group_id>\d+)/(?P<post_id>\d+)/$',
        views.edit_post,
        name='editpost'
    ),
    url(
        r'^(?P<group_id>\d+)/approvepost/$',
        views.approve_post,
        name='approvepost'
    ),
    url(
        r'^(?P<group_id>\d+)/approvecomment/$',
        views.approve_comment,
        name='approvecomment'
    ),
    url(
        r'^group/notapprovedcomments/(?P<group_id>\d+)/$',
        views.notapproved_comment_admin_page,
        name='notapprovedcomments'
    ),
    url(
        r'^group/approvedcomments/(?P<group_id>\d+)/$',
        views.approved_comment_admin_page,
        name='approvedcomments'
    ),
    url(
        r'^group/editcomment/(?P<group_id>\d+)/(?P<comment_id>\d+)/$',
        views.edit_comment_admin_page,
        name='editcomment'
    ),
    url(
        r'^group/joinrequests/(?P<group_id>\d+)/$',
        views.joinrequest_admin_page,
        name='joinrequest'
    ),
    url(
        r'^group/members/(?P<group_id>\d+)/$',
        views.group_member_page,
        name='members'
    ),
    url(
        r'^group/bannedmembers/(?P<group_id>\d+)/$',
        views.group_banned_members_page,
        name='bannedmembers'
    ),
    url(
        r'^group/userautocomplete/(?P<group_id>\d+)/$',
        views.users_autocomplete,
        name='users_autocomplete'
    ),
    url(
        r'^group/inviteuser/(?P<group_id>\d+)/$',
        views.invite_user,
        name='inviteuser'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/events/$',
        views.group_events_admin_page,
        name='eventsadmin'
    ),
    url(
        r'^group/createnotification/(?P<group_id>\d+)/$',
        views.create_notification_admin,
        name='createnotification'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/dashboard/$',
        views.group_dashboard_admin_page,
        name='groupdashboard'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/defaultroles/$',
        views.group_default_role_admin_page,
        name='groupdefaultrole'
    ),
    url(
        r'^group/(?P<group_id>\d+)/admin/customroles/$',
        views.group_custom_role_admin_page,
        name='groupcustomrole'
    ),
    url(
        r'^group/editroleperm/(?P<group_id>\d+)/(?P<custom_role_id>\d+)/$',
        views.edit_permissions,
        name='editperm'
    ),
    url(
        r'^group/edituserperm/(?P<group_id>\d+)/(?P<user_id>\d+)/$',
        views.edit_extra_permissions,
        name='edituserperm'
    ),
    url(
        r'^group/edittoggle/(?P<group_id>\d+)/$',
        views.group_admin_settings_toggle,
        name='edittoggle'
    ),
    url(
        r'^integrate_users/$',
        views.integrate_users
    )
]
