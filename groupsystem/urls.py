from django.conf.urls import url
from groupsystem import views


urlpatterns = [
    url(r'^groups/$', views.all_group_page, name='allgroups'),
    url(r'^joinedgroups/$', views.joined_group_page, name='joinedgroups'),
    url(r'^subscribedgroups/$', views.user_group_page, name='subscribedgroups'),
    url(r'^creategroup/$', views.create_group, name='creategroup'),
    url(r'^group/(?P<id>\d+)/$', views.basic_group_details, name='groupdetails'),
    url(r'^(?P<group_id>\d+)/n/(?P<id>\d+)/$', views.news_details, name='newsdetails'),
    url(r'^group/(?P<id>\d+)/events/$', views.group_events_page, name='events'),
    url(r'^group/(?P<id>\d+)/groupposts/$', views.group_admin_post_page, name='adminposts'),
    url(r'^group/(?P<id>\d+)/groupposts/membercreated/$', views.group_member_post_page, name='memberposts'),
    url(r'^group/(?P<group_id>\d+)/groupposts/(?P<post_id>\d+)/$', views.postdetails_page, name='postdetail'),
    url(r'^(?P<group_id>\d+)/l/(?P<post_id>\d+)/$', views.like_post, name='like'),
    url(r'^c/(?P<group_id>\d+)/(?P<post_id>\d+)/$', views.comment_post, name='comment'),
    url(
        r'^creatememberpost/(?P<group_id>\d+)/$',
        views.create_member_post,
        name='creatememberpost'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/settings/$',
        views.group_admin_settings_page,
        name='adminsettings'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/news/$',
        views.group_admin_news_page,
        name='adminnews'
    ),
    url(
        r'^(?P<group_id>\d+)/editnews/$',
        views.edit_news,
        name='editnews'
    ),
    url(
        r'^group/(?P<id>\d+)/grouppostsadmin/$',
        views.groupadmin_admin_post_page,
        name='adminpostsadmin'
    ),
    url(
        r'^group/(?P<id>\d+)/grouppostsadmin/membercreated/$',
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
        views.edit_post_admin_page,
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
        r'^notapprovedcomments/(?P<group_id>\d+)/$',
        views.notapproved_comment_admin_page,
        name='notapprovedcomments'
    ),
    url(
        r'^approvedcomments/(?P<group_id>\d+)/$',
        views.approved_comment_admin_page,
        name='approvedcomments'
    ),
    url(
        r'^editcomment/(?P<group_id>\d+)/(?P<comment_id>\d+)/$',
        views.edit_comment_admin_page,
        name='editcomment'
    ),
    url(
        r'^joinrequests/(?P<group_id>\d+)/$',
        views.joinrequest_admin_page,
        name='joinrequest'
    ),
    url(
        r'^members/(?P<group_id>\d+)/$',
        views.group_member_page,
        name='members'
    ),
    url(
        r'^bannedmembers/(?P<group_id>\d+)/$',
        views.group_banned_members_page,
        name='bannedmembers'
    ),
    url(
        r'^userautocomplete/(?P<group_id>\d+)/$',
        views.users_autocomplete,
        name='users_autocomplete'
    ),
    url(
        r'^inviteuser/(?P<group_id>\d+)/$',
        views.invite_user,
        name='inviteuser'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/events/$',
        views.group_events_admin_page,
        name='eventsadmin'
    ),
    url(
        r'^createnotification/(?P<group_id>\d+)/$',
        views.create_notification_admin,
        name='createnotification'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/dashboard/$',
        views.group_dashboard_admin_page,
        name='groupdashboard'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/defaultroles/$',
        views.group_default_role_admin_page,
        name='groupdefaultrole'
    ),
    url(
        r'^(?P<group_id>\d+)/admin/customroles/$',
        views.group_custom_role_admin_page,
        name='groupcustomrole'
    ),
    url(
        r'^editroleperm/(?P<group_id>\d+)/(?P<custom_role_id>\d+)/$',
        views.edit_permissions,
        name='editperm'
    ),
    url(
        r'^edituserperm/(?P<group_id>\d+)/(?P<user_id>\d+)/$',
        views.edit_extra_permissions,
        name='edituserperm'
    ),
]
