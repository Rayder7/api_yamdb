import uuid

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb import settings
from reviews.models import (
    Category, Genre, Review, Title, User
)
from .mixins import CRDViewSet
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleSerializerRead, TitleSerializerCreate, UserSerializer,
    SignupSerializer, TokenSerializer
)
from .filters import TitleFilter
from .permissions import IsAdminOnly, ReadOnly, IsAuthorOrModeratorOrReadOnly


class CategoryViewSet(CRDViewSet):
    """Вьюсет для CategorySerializer."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CRDViewSet):
    """Вьюсет для GenreSerializer."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для TitleSerializer."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializerCreate
    permission_classes = (IsAdminOnly | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ReviewSerializer."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CommentSerializer."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для UserSerializer."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer
    )
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def Token(request):
    """Метод получения токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirm_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if user.confirmation_code != confirm_code:
        return Response(
            'Код неверный', status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    token_data = {'token': str(refresh.access_token)}

    return Response(token_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
    """Метод авторизации через отправку письма."""
    serializer = SignupSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    try:
        user, created = User.objects.get_or_create(
            **serializer.validated_data,
            confirmation_code=confirmation_code
        )
    except Exception as error:
        return Response(
            f'Получена ошибка ->{error}<-',
            status=status.HTTP_400_BAD_REQUEST
        )
    send_mail(
        subject='Код подтверждения',
        message=f'{user.confirmation_code} - Код авторизации на сайте',
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
