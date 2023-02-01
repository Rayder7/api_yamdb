from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<id>\d+)/reviews/(?P<id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
