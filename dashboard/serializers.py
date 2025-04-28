from rest_framework import serializers


class BillingReportSerializer(serializers.Serializer):
    staff_name = serializers.CharField(
        source="created_by__name"
    )  # Represents the user's name (created_by)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )  # Represents the total sales amount
    medicines_billed = (
        serializers.IntegerField()
    )  # Represents the number of medicines billed
