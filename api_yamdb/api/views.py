from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer)
from .permissions import IsAdminOnly#, OwnerOrModeratorOrAdminUserPermission


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('id')
        # title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    #permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('id')
        return Comment.objects.filter(id=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    serializer_class = UserSerializer
    pass


class Token():
    pass


class Signup():
    pass
