from rest_framework.viewsets import ModelViewSet
from medical_billing.permissions import IsInventoryManager
from medicine_management.models import Medicine
from medicine_management.serializers import (
    MedicineSerializer,
    MedicineListSerializer,
)


class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = (IsInventoryManager,)

    def get_queryset(self):
        if self.action == "update":
            return MedicineSerializer.setup_eager_loading(
                Medicine.objects.all()
            )
        if self.action == "list":
            return Medicine.objects.prefetch_related("package_types__batches")
        return Medicine.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MedicineListSerializer
        return MedicineSerializer
