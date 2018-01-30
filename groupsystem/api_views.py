from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.serializers import GroupSerializer
from groupsystem.models import BasicGroup


def _make_group_serializable(group):
    data = {
        'id': group.id,
        'group_url': group.get_absolute_url(),
        'name': group.name,
        'description': group.short_about,
        'group_type': group.group_type_other
        if group.get_group_type_display() == 'Other'
        else group.get_group_type_display(),
        # 'header_image_url': group.header_image.thumbnail["300x100"].url,
        'logo_url': group.logo.thumbnail["92x92"].url,
        'members': [user.username for user in group.members.all()],
        'subscribers': [user.username for user in group.subscribers.all()],
    }
    return data


class GroupsView(APIView):
    """
    This view returns all groups

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        basicgroups = BasicGroup.objects.all()
        datas = []
        for basicgroup in basicgroups:
            data = _make_group_serializable(basicgroup)
            datas.append(data)
        serializer = GroupSerializer(datas, many=True)
        return Response(serializer.data)


class GroupSubscribeView(APIView):
    """
    This view will subscribe/unsubscribe user from a group

    * Required logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, group_id, format=None):
        try:
            basicgroup = BasicGroup.objects.get(id=group_id)
            data = {
                "subscribed": True,
                "username": request.user.username,
                "group_id": basicgroup.id
            }
            if request.data.get('subscribe'):
                basicgroup.subscribers.add(request.user)
                subscriber_group = Group.objects.get(
                    name='%s_subscriber' % basicgroup.id
                )
                request.user.groups.add(subscriber_group)
                return Response(data)        
            else:
                basicgroup.subscribers.remove(request.user)
                subscriber_group = Group.objects.get(
                    name='%s_subscriber' % basicgroup.id
                )
                request.user.groups.remove(subscriber_group)
                data["subscribed"] = False
                return Response(data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
