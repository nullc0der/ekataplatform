from rest_framework import permissions


class IsAdminOfGroup(permissions.BasePermission):
    """
    Checks if user is admin of the group
    """
    def has_object_permission(self, request, view, obj):
        return request.user in set(
            obj.super_admins.all() |
            obj.admins.all()
        )
