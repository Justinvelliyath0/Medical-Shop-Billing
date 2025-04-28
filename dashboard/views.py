from datetime import datetime

from django.db.models import Sum, Q, Count
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from billing.models import Bill
from dashboard.serializers import BillingReportSerializer
from medical_billing.permissions import IsAdmin
from medicine_management.models import Medicine
from medicine_management.serializers import MedicineListSerializer


class StockListView(ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = MedicineListSerializer
    queryset = Medicine.objects.all()


class BillingReportView(ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = BillingReportSerializer

    def get_queryset(self):

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        queryset = Bill.objects.values(
            "created_by__id", "created_by__name"
        ).annotate(
            medicines_billed=Count("bill__medicine", distinct=True),
            total_amount=Sum("bill__total_price"),
        )

        queryset = queryset.filter(created_by__role="STAFF")
        if start_date or end_date:
            date_filters = Q()
            try:
                if start_date:
                    start_date = datetime.strptime(
                        start_date, "%Y-%m-%d"
                    ).date()
                    date_filters &= Q(created_at__gte=start_date)

                if end_date:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    date_filters &= Q(created_at__lte=end_date)

                queryset = queryset.filter(date_filters)
            except ValueError:
                raise ValidationError(
                    {"date_error": "Invalid date format. Use YYYY-MM-DD."},
                    code="invalid_date",
                )
        return queryset
