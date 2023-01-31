from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
