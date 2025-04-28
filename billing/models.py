from django.db import models

from medicine_management.models import Medicine
from users.models import User


class Bill(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "bill"


class BillItem(models.Model):
    PACKAGE_TYPES = (
        ("single", "Single Piece/Strip"),
        ("pack", "Pack"),
        ("box", "Box"),
    )
    bill = models.ForeignKey(
        Bill, null=True, on_delete=models.CASCADE, related_name="bill"
    )
    medicine = models.ForeignKey(
        Medicine, null=True, on_delete=models.SET_NULL, related_name="medicine"
    )
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    batches_used = models.JSONField(default=list)

    class Meta:
        db_table = "bill_item"
