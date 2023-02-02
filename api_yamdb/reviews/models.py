from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=60)


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
