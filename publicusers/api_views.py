from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from publicusers.serializers import UserSerializer


def _make_user_serializeable(user):
    data = {
        'id': user.id,
        'username': user.username,
        'fullname': user.get_full_name(),
        'is_online': user.profile.online(),
        'user_image_url':
            user.profile.avatar.thumbnail['82x82'].url if user.profile.avatar else "",
        'user_avatar_color': user.profile.default_avatar_color,
        'public_url': user.profile.get_public_profile_url(),
        'is_staff': user.is_staff
    }
    return data


class UsersListView(APIView):
    """
    View to return all members and staff

    * Only logged in users will be able to access this view
    """

    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        """
        Returns list of members and staff excluding request.user
        and AnonymousUser
        """
        datas = []
        users = User.objects.exclude(
            username__in=['AnonymousUser', request.user.username]
        )
        for user in users:
            data = _make_user_serializeable(user)
            datas.append(data)
        serializer = UserSerializer(datas, many=True)
        return Response(serializer.data)
