from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_username

User = get_user_model()

class Category(models.Model):
    name = models.CharField('Название', max_length=256, default='отсутствует')
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField('Дата выпуска')
    description = models.TextField('Описание', blank=True, null=True)
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
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class User(AbstractUser):
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
        validators=[validate_username])
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
        return (self.role == self.ADMIN or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.MODER

    def __str__(self):
        return self.username


class Rating(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating_author'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='rating_title'
    )

    def __str__(self):
        return f'{self.title}- {self.author}'

    class Meta:
        unique_together = ('author', 'title')


class Review(models.Model):
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='review_author'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.ForeignKey(
        Rating, validators=[MinValueValidator(1), MaxValueValidator(10)], on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.text[:15]} - {self.score}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField('Комментарий', max_length=5000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comment_author'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

