from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comment
from .permissions import OwnerOrModeratorOrAdminUserPermission


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('id')
        # title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(id=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('id')
        return Comment.objects.filter(id=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

