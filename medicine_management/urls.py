from rest_framework import routers
from medicine_management.views import MedicineViewSet

router = routers.SimpleRouter()

router.register(r"", MedicineViewSet)

urlpatterns = router.urls
