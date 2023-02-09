from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import (
    max_length_validator, validate_username, year_validator
)

VALUE_MIN_VAL = 1
VALUE_MAX_VAL = 10


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField('Название', max_length=256, default='отсутствует')
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Названия произведений, к которым пишутся отзывы.
    """
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Дата выпуска', validators=(year_validator,)
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreToTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='categories'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Доп.таблица для связи ManyToMany."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.title} + {self.genre}'


class User(AbstractUser):
    """Пользователи."""
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODER, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    email = models.EmailField('Почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Код для идентификации'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_together'
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODER

    def __str__(self):
        return self.username


class Review(models.Model):
    """Отзывы к произведениям."""
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='review_author'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=(
            MinValueValidator(VALUE_MIN_VAL), MaxValueValidator(VALUE_MAX_VAL)
        ),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return f'{self.text} - {self.score}'


class Comment(models.Model):
    """Комментарии к произведениям."""
    text = models.TextField('Комментарий', validators=(max_length_validator,))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comment_author'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
