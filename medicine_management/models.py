from django.db import models

from users.models import User


# Create your models here.


class Medicine(models.Model):
    CATEGORY_CHOICES = (
        ("painkiller", "Painkiller"),
        ("antibiotic", "Antibiotic"),
        ("other", "Other"),
    )
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "medicines"
        indexes = [
            models.Index(fields=["name", "generic_name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.generic_name})"


class PackageTypes(models.Model):
    PACKAGE_TYPES = (
        ("single", "Single Piece/Strip"),
        ("pack", "Pack"),
        ("box", "Box"),
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="package_types"
    )
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "medicine_package_type"
        unique_together = ("medicine", "package_type")

    def __str__(self):
        return f"{self.medicine.name} - \
                package type: {self.get_package_type_display()}"


class Batch(models.Model):
    package_type = models.ForeignKey(
        PackageTypes, on_delete=models.CASCADE, related_name="batches"
    )
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    purchase_date = models.DateField()

    class Meta:
        db_table = "medicine_batch"
        indexes = [models.Index(fields=["expiry_date"])]

    def __str__(self):
        return f"Batch {self.id} - Expiry {self.expiry_date}"
