from django.conf.urls import url
from eblast import views


urlpatterns = [
    url(r'^emailgroups/$', views.emailgroups_page, name='emailgroups'),
    url(r'^create_emailgroup/$', views.create_emailgroup, name='create_emailgroup'),
    url(r'^delete_emailgroup/$', views.delete_emailgroup, name='delete_emailgroup'),
    url(r'^add_user/(?P<id>\d+)/$', views.add_user_to_emailgroup, name='add_user_to_emailgroup'),
    url(r'^add_csv/(?P<id>\d+)/$', views.add_csv_to_emailgroup, name='add_csv_to_emailgroup'),
    url(r'^change_group_name/$', views.change_group_name, name='change_group_name'),
    url(r'^remove_emailid/$', views.remove_emailid, name='remove_emailid'),
    url(r'^unsubscribe_emailid/$', views.unsubscribe_emailid, name='unsubscribe_emailid'),
    url(r'^subscribe_emailid/$', views.subscribe_emailid, name='subscribe_emailid'),
    url(r'^filter_groups/$', views.filter_groups, name='filter_groups'),
    url(r'^emailtemplates/$', views.emailtemplates_page, name='emailtemplates'),
    url(r'^add_emailtemplate/$', views.add_emailtemplate, name='add_emailtemplate'),
    url(r'^delete_emailtemplate/$', views.delete_emailtemplate, name='delete_emailtemplate'),
    url(r'^edit_emailtemplate/(?P<id>\d+)/$', views.edit_emailtemplate, name='edit_emailtemplate'),
    url(r'^preview_emailtemplate/(?P<id>\d+)/$', views.preview_emailtemplate, name='preview_emailtemplate'),
    url(r'^change_template_name/$', views.change_template_name, name='change_template_name'),
    url(r'^filter_template/$', views.filter_template, name='filter_template'),
    url(r'^campaigns/$', views.emailcampaign_page, name='emailcampaign_page'),
    url(r'^add_emailcampaign/$', views.add_emailcampaign, name='add_emailcampaign'),
    url(r'^edit_emailcampaign/(?P<id>\d+)/$', views.edit_emailcampaign, name='edit_emailcampaign'),
    url(r'^delete_emailcampaign/$', views.delete_emailcampaign, name='delete_emailcampaign'),
    url(r'^test_send_campaign/(?P<id>\d+)/$', views.test_send_campaign, name='test_send_campaign'),
    url(r'^send_campaign/(?P<id>\d+)/$', views.send_campaign, name='send_campaign'),
    url(r'^campaign/(?P<id>\d+)/$', views.view_email_in_browser, name='viewinbrowser'),
    url(r'^image/(?P<campaign_id>\d+)/(?P<reciever_id>\d+)/$', views.get_campaign_image_link, name='get_campaign_image_link'),
    url(r'^campaign_tracking_data/$', views.campaign_tracking_data, name='campaign_tracking_data'),
    url(r'^change_campaign_name/$', views.change_campaign_name, name='change_campaign_name'),
    url(r'^filter_campaign/$', views.filter_campaign, name='filter_campaign'),
]
