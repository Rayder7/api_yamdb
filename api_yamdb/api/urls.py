from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
v1_router = DefaultRouter()

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    #path('v1/auth/signup/', думаю, name='signup'),
    #path('v1/auth/token/', думаю, name='token'),
]