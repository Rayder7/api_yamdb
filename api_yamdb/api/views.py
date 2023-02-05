from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, authentication, exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer, SignupSerializer)
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
    pagination_class = LimitOffsetPagination
    # permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (OwnerOrModeratorOrAdminUserPermission,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    serializer_class = UserSerializer
    pass


class Token():
    pass


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        keys = serializer.data.keys()
        if 'email' not in keys or 'username' not in keys:
            raise exceptions.ValidationError('Missing required field email or username')
        email = serializer.data['email']
        username = serializer.data['username']
        user = User.objects.filter(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        serializer.save()
        send_mail(
            'Your code to yamdb',
            f'your confirmation code{confirmation_code}',
            'test@mail.com',
            [f'{email}']
        )



