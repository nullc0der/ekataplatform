from rest_framework import permissions


class IsOwnerOfPost(permissions.BasePermission):
    """
    Checks if user is owner of post
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsOwnerOfComment(permissions.BasePermission):
    """
    Checks if user is owner of comment
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.commentor
