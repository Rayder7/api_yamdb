from django.contrib import admin

from reviews.models import Review, Comment

admin.site.register(Review)
admin.site.register(Comment)

