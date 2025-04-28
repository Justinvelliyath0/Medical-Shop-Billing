from rest_framework import serializers

from billing.models import Bill, BillItem


class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = (
            "bill",
            "medicine",
            "package_type",
            "quantity",
            "unit_price",
            "total_price",
            "batches_used",
        )


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ("total_amount", "created_by")
