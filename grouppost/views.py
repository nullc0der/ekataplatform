from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework import parsers
from rest_framework.response import Response

from profilesystem.permissions import IsAuthenticatedLegacy
from groupsystem.permissions import (
    IsMemberOfGroup, IsModeratorOfGroup)
from groupsystem.models import BasicGroup, GroupPost, PostComment
from grouppost.forms import ImageForm
from grouppost.serializers import PostSerializer, CommentSerialzer
from grouppost.permissions import (
    IsOwnerOfPostOrModeratorOfGroup, IsOwnerOfCommentOrModeratorOfGroup,
    IsOwnerOfObjectOrModeratorOfGroup)


# Create your views here.

def get_approver_set(basicgroup):
    return set(  # NOTE: not sure why the | needed, research
        basicgroup.super_admins.all() |
        basicgroup.admins.all() |
        basicgroup.staffs.all() |
        basicgroup.moderators.all()
    )


class PostViewSets(viewsets.ViewSet):
    """
    API viewsets for Group Post feature
    """

    def get_permissions(self):
        permission_classes = (IsAuthenticatedLegacy, IsMemberOfGroup)
        if self.action == 'update' or self.action == 'destroy':
            permission_classes = (
                IsAuthenticatedLegacy, IsOwnerOfPostOrModeratorOfGroup)
        if self.action == 'partial_update':
            permission_classes = (IsAuthenticatedLegacy, IsModeratorOfGroup)
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            basicgroup = BasicGroup.objects.get(id=request.GET.get('groupID'))
            self.check_object_permissions(request, basicgroup)
            request.session['basicgroup'] = basicgroup.id
            if request.user in get_approver_set(basicgroup):
                queryset = basicgroup.posts.all()
            else:
                queryset = set(basicgroup.posts.filter(approved=True) |
                               basicgroup.posts.filter(creator=request.user))
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            basicgroup = BasicGroup.objects.get(id=request.data.get('groupID'))
            self.check_object_permissions(request, basicgroup)
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                if request.user in get_approver_set(basicgroup)\
                        or basicgroup.auto_approve_post:
                    serializer.save(
                        creator=request.user, basic_group=basicgroup,
                        approved=True
                    )
                else:
                    serializer.save(
                        creator=request.user, basic_group=basicgroup
                    )
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            post = GroupPost.objects.get(id=pk)
            self.check_object_permissions(request, post)
            return Response(
                PostSerializer(post).data
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            post = GroupPost.objects.get(id=pk)
            self.check_object_permissions(request, post)
            serializer = PostSerializer(post, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            post = GroupPost.objects.get(id=pk)
            self.check_object_permissions(request, post)
            serializer = PostSerializer(post, request.data, partial=True)
            if serializer.is_valid():
                serializer.save(
                    approved=True,
                    approved_by=request.user
                )
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = GroupPost.objects.get(id=pk)
            self.check_object_permissions(request, post)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewset(viewsets.ViewSet):
    """
    API Viewset for comments
    """

    def get_permissions(self):
        permission_classes = (IsAuthenticatedLegacy, IsMemberOfGroup)
        if self.action == 'update':
            permission_classes = (
                IsAuthenticatedLegacy, IsOwnerOfCommentOrModeratorOfGroup)
        if self.action == 'partial_update':
            permission_classes = (IsAuthenticatedLegacy, IsModeratorOfGroup)
        if self.action == 'destroy':
            permission_classes = (
                IsAuthenticatedLegacy, IsOwnerOfObjectOrModeratorOfGroup)
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            post = GroupPost.objects.get(id=request.GET.get('postID'))
            self.check_object_permissions(request, post)
            if request.user in get_approver_set(post.basic_group):
                comments = post.comments.all()
            else:
                comments = set(post.comments.filter(approved=True) |
                               post.comments.filter(commentor=request.user))
            serializer = CommentSerialzer(comments, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            post = GroupPost.objects.get(id=request.data.get('postID'))
            self.check_object_permissions(request, post)
            serializer = CommentSerialzer(data=request.data)
            if serializer.is_valid():
                if request.user in get_approver_set(post.basic_group)\
                        or post.basic_group.auto_approve_comment:
                    serializer.save(
                        post=post, commentor=request.user, approved=True
                    )
                else:
                    serializer.save(
                        post=post, commentor=request.user
                    )
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            comment = PostComment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            serializer = CommentSerialzer(comment, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            comment = PostComment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            serializer = CommentSerialzer(comment, request.data, partial=True)
            if serializer.is_valid():
                serializer.save(
                    approved=True,
                    approved_by=request.user
                )
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            comment = PostComment.objects.get(id=pk)
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UploadImage(APIView):
    """
    This view saves an image for post

    * Permissions Required
        * Logged in user
    """
    permission_classes = (IsAuthenticatedLegacy, )
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser)

    def post(self, request, format=None):
        if request.data.get('image'):
            imageform = ImageForm(request.POST, request.FILES)
            if imageform.is_valid():
                image = imageform.save(commit=False)
                image.uploader = request.user
                image.save()
                return Response(
                    image.image.url
                )
        return Response()
