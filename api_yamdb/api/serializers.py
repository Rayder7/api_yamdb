from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title, User

VALUE_MIN_VAL = 1
VALUE_MAX_VAL = 10


class CategorySerializer(serializers.ModelSerializer):
    """Серилизатор для модели Category."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Серилизатор для модели Genre."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerRead(serializers.ModelSerializer):
    """Серилизатор для модели Title только чтение."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre'
        )
        model = Title

    def get_rating(self, obj):
        avg = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return avg['score__avg']


class TitleSerializerCreate(serializers.ModelSerializer):
    """Серилизатор для модели Title создание."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    """Серилизатор для модели User."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            validate_username,
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            ),
        ]


class SignupSerializer(serializers.Serializer):
    """Серилизатор для авторизации с помощью e-mail."""
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )


class TokenSerializer(serializers.Serializer):
    """Серилизатор для токена."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для модели Review."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    score = serializers.IntegerField(
        required=True,
        validators=(
            MaxValueValidator(VALUE_MAX_VAL),
            MinValueValidator(VALUE_MIN_VAL))
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if title.reviews.filter(title=title_id, author=author).exists():
                raise ValidationError('only one review to title')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Серилизатор для модели Comment."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'review')
        exclude = ('review',)
