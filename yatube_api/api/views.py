#  Импортируйте в код всё необходимое
from rest_framework import viewsets, pagination, filters
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer
)

from .permissions import ApiPermission, GroupPermission


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [ApiPermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [ApiPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_post_obj().comments.all()

    def get_post_obj(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_pk')
        )

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=self.get_post_obj()
        )


class GroupViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [GroupPermission]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )
