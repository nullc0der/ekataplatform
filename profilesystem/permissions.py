from rest_framework import permissions


class IsAuthenticatedLegacy(permissions.BasePermission):
    """
    This permission check class is for django < 1.11
    """
    def has_permission(self, request, view):
        """
        is_authenticated is a method in django 1.9 not an property
        """
        return request.user and request.user.is_authenticated()
