from rest_framework import viewsets

from .permission import IsAdminOnly
from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    serializer_class = UserSerializer
    pass


class Token():
    pass


class Signup():
    pass
