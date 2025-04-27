from rest_framework import mixins, viewsets
from medical_billing.permissions import IsAdmin
from users.models import User
from users.serializers import UserSerializer, UserListSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer
