from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import (
    CustomTokenObtainPairSerializer,
    CreateUserSerializer,
)
from medical_billing.permissions import IsAdmin
from users.models import User


class LoginApi(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = CreateUserSerializer
