from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Review, Comment, User


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
