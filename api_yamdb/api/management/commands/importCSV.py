import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, GenreToTitle, Title, User


class Command(BaseCommand):
    '''Комнда для импорта данных из .csv'''
    def category_transfer(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/category.csv'),
                  'r', encoding='utf-8') as csv_f:
            file_reader = csv.reader(csv_f, delimiter=",")

            for r in file_reader:
                if r[0] != 'id':
                    Category.objects.get_or_create(
                        id=r[0], name=r[1], slug=r[2]
                    )

    def genre_transfer(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/genre.csv'),
                  'r', encoding='utf-8') as csv_f:
            file_reader = csv.reader(csv_f, delimiter=",")

            for r in file_reader:
                if r[0] != 'id':
                    Genre.objects.get_or_create(
                        id=r[0], name=r[1], slug=r[2]
                    )

    def title_transfer(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/titles.csv'),
                  'r', encoding='utf-8') as csv_f:
            file_reader = csv.reader(csv_f, delimiter=",")

            for r in file_reader:
                if r[0] != 'id':
                    Title.objects.get_or_create(
                        id=r[0], name=r[1], year=r[2],
                        category_id=r[3]
                    )

    def title_genre_transfer(self):
        with open(os.path.join(
            settings.BASE_DIR, 'static/data/genre_title.csv'
        ), 'r', encoding='utf-8') as csv_f:

            file_reader = csv.reader(csv_f, delimiter=",")

            for r in file_reader:
                if r[0] != 'id':
                    GenreToTitle.objects.get_or_create(
                        id=r[0], title_id=r[1], genre_id=r[2]
                    )

    def user_transfer(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/users.csv'),
                  'r', encoding='utf-8') as csv_f:
            file_reader = csv.reader(csv_f, delimiter=",")

            for r in file_reader:
                if r[0] != 'id':
                    User.objects.get_or_create(
                        id=r[0], username=r[1], email=r[2],
                        role=r[3], bio=r[4],
                        first_name=[5], last_name=r[6]
                    )

    def handle(self, *args, **options):
        self.category_transfer()
        self.genre_transfer()
        self.title_transfer()
        self.title_genre_transfer()
        #  self.user_transfer() не работает: django.db.utils.OperationalError:
        #  no such table: reviews_user
