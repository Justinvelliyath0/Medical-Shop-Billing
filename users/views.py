from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from medical_billing.permissions import IsAdmin
from users.models import User
from users.serializers import (
    UserSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "update":
            return UserUpdateSerializer
        return UserSerializer
