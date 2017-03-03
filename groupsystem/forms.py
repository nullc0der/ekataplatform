import bleach

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from groupsystem.models import BasicGroup, GroupPost, GroupNews,\
    PostComment, GroupNotification, CustomRole,\
    GroupMemberExtraPerm


class CreateGroupForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        try:
            BasicGroup.objects.get(name=name)
        except ObjectDoesNotExist:
            return name
        raise forms.ValidationError(
            _('Group Exist')
        )

    def clean_group_type_other(self):
        group_type = self.cleaned_data.get('group_type', None)
        group_type_other = self.cleaned_data.get('group_type_other', None)

        if group_type == '9':
            if group_type_other:
                return group_type_other
            else:
                raise forms.ValidationError(
                    _('You must specify other group type')
                )

        if group_type != '9':
            if group_type_other:
                raise forms.ValidationError(
                    _("You can't fill this field with default group types")
                )

    class Meta:
        model = BasicGroup
        fields = [
            'name',
            'short_about',
            'group_type',
            'group_type_other'
        ]


class CreatePostForm(forms.ModelForm):
    def clean_post(self):
        post = self.cleaned_data.get('post', '')
        cleaned_text = bleach.clean(
            post,
            settings.BLEACH_VALID_TAGS,
            settings.BLEACH_VALID_ATTRS,
            settings.BLEACH_VALID_STYLES
        )
        return cleaned_text  # sanitize html

    class Meta:
        model = GroupPost
        fields = [
            'title',
            'post'
        ]


class EditGroupForm(forms.ModelForm):
    header_image = forms.ImageField(
        required=False,
        widget=forms.FileInput
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput
    )

    def __init__(self, *args, **kwargs):
        self.basicgroup = kwargs.pop('basicgroup', None)
        super(EditGroupForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        if self.basicgroup.name == name:
            return name
        else:
            try:
                BasicGroup.objects.get(name=name)
            except ObjectDoesNotExist:
                return name
        raise forms.ValidationError(
            _('Group name already taken')
        )

    def clean_group_type_other(self):
        group_type = self.cleaned_data.get('group_type', None)
        group_type_other = self.cleaned_data.get('group_type_other', None)

        if group_type == '9':
            if group_type_other:
                return group_type_other
            else:
                raise forms.ValidationError(
                    _('You must specify other group type')
                )

        if group_type != '9':
            if group_type_other:
                raise forms.ValidationError(
                    _("You can't fill this field with default group types")
                )

    class Meta:
        model = BasicGroup
        fields = [
            'name',
            'header_image',
            'logo',
            'short_about',
            'long_about',
            'group_type',
            'group_type_other',
        ]


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = GroupNews
        fields = ['title', 'news']


class EditPostForm(forms.ModelForm):
    def clean_post(self):
        post = self.cleaned_data.get('post', '')
        cleaned_text = bleach.clean(
            post,
            settings.BLEACH_VALID_TAGS,
            settings.BLEACH_VALID_ATTRS,
            settings.BLEACH_VALID_STYLES
        )
        return cleaned_text  # sanitize html

    class Meta:
        model = GroupPost
        fields = [
            'title',
            'post',
        ]


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = [
            'comment',
        ]


class EventForm(forms.Form):
    event_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(label="Title", max_length=60, required=True)
    start_date = forms.DateTimeField(
        required=True,
        label='Start Date',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker'
            }
        )
    )
    end_date = forms.DateTimeField(
        required=False,
        label='End Date',
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker'
            }
        )
    )
    color = forms.CharField(label='Color', required=True)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = GroupNotification
        fields = [
            'notification'
        ]


class CustomRoleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.group_id = kwargs.pop('group_id', None)
        super(CustomRoleCreateForm, self).__init__(*args, **kwargs)

    def clean_custom_role_name(self):
        restricted_names = ['superadmin', 'admin', 'moderator', 'member', 'subscriber']
        custom_role_name = self.cleaned_data.get('custom_role_name', None)
        if custom_role_name.lower() in restricted_names:
            raise forms.ValidationError(
                _(
                    "You can't choose a default role name"
                )
            )
        try:
            CustomRole.objects.get(permission_group='%s_%s' % (self.group_id, custom_role_name))
        except ObjectDoesNotExist:
            return custom_role_name
        raise forms.ValidationError(_("Role exist"))

    class Meta:
        model = CustomRole
        fields = [
            'custom_role_name'
        ]


class EditRolePermForm(forms.ModelForm):
    class Meta:
        model = CustomRole
        exclude = [
            'basic_group',
            'custom_role_name',
            'permission_group'
        ]


class EditExtraPermForm(forms.ModelForm):
    class Meta:
        model = GroupMemberExtraPerm
        exclude = [
            'basic_group',
            'user'
        ]
