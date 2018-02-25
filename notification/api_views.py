
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from notification.models import Notification
from notification.utils import get_serialized_notification


class NotificationView(APIView):
    """
    This view returns list of unread notifications of
    request.user

    * Permission required:
        * Logged in user
    """

    permission_classes = (IsAuthenticatedLegacy, )

    def get(self, request, format=None):
        datas = []
        notifications = Notification.objects.filter(
            user=request.user,
            read=False
        )
        for notification in notifications:
            datas.append(get_serialized_notification(notification))
        return Response(datas)


class NotificationDetailView(APIView):
    """
    This view makes a notification or list of notifications
    read/unread
    * Permission required
        * Logged in user
    """

    permission_classes = (IsAuthenticatedLegacy, )

    def post(self, request, format=None):
        id_lists = request.data.get('idlist', None)
        processed_ids = []
        for notification_id in id_lists:
            try:
                notification = Notification.objects.get(id=notification_id)
                if notification.user == request.user:
                    notification.read = True
                    if hasattr(notification.content_object, 'read'):
                        notification.content_object.read = True
                        notification.content_object.save()
                    notification.save()
                    processed_ids.append(notification_id)
            except ObjectDoesNotExist:
                pass
        return Response(processed_ids)
