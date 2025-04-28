from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.serializers import BillSerializer
from billing.services import BillingService
from medical_billing.permissions import IsStaff


class CreateBillView(APIView):
    permission_classes = (IsStaff,)

    def post(self, request):
        try:
            bill = BillingService.create_bill(
                request.user, request.data["items"]
            )
            serializer = BillSerializer(bill)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
