from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]


class SignupSerializer(serializers.Serializer):
    pass


class TokenSerializer(serializers.Serializer):
    pass
  
  
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault,
        queryset=User.objects.all(),
        slug_field='username'
    )
    score = serializers.IntegerField(
        required=True,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('title', 'author')

    def validate_title(self, value):
        if value == self.context.get('request').pk:  # под вопросом, как это сделать?
            raise serializers.ValidationError()
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault,
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'review')
        exclude = ('review',)
