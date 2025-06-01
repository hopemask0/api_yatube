from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedForSafeMethods
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer
)
from posts.models import Post, Group, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedForSafeMethods,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedForSafeMethods]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedForSafeMethods,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)
