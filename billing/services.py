from collections import defaultdict

from django.db import transaction

from medicine_management.models import PackageTypes, Batch
from .models import Bill, BillItem


class BillingService:
    @staticmethod
    @transaction.atomic
    def create_bill(user, items_data):
        bill = Bill.objects.create(created_by=user, total_amount=0)
        total_amount = 0

        medicine_ids = {item["medicine_id"] for item in items_data}
        packages = PackageTypes.objects.filter(
            medicine_id__in=medicine_ids
        ).select_related("medicine")

        package_types = {}
        package_ids = []
        bill_items = []

        for p in packages:
            package_types[(p.medicine_id, p.package_type)] = p
            package_ids.append(p.id)

        batches_by_pkg = (
            Batch.objects.filter(
                package_type_id__in=package_ids, quantity__gt=0
            )
            .order_by("expiry_date")
            .only("id", "quantity", "expiry_date", "package_type_id")
        )
        batches = defaultdict(list)
        for b in batches_by_pkg:
            batches[b.package_type_id].append(b)

        batches_to_update = []

        for item_data in items_data:
            package_type = package_types.get(
                (item_data["medicine_id"], item_data["package_type"]), None
            )
            if package_type is None:
                raise ValueError(
                    f"Package type ({item_data["package_type"]}) "
                    f"Does not exist"
                )

            batches_used = []
            remaining_qty = item_data["quantity"]

            for batch in batches.get(package_type.id, []):
                if remaining_qty <= 0:
                    break

                deduct_qty = min(remaining_qty, batch.quantity)
                batch.quantity -= deduct_qty
                batches_used.append(
                    {
                        "batch_id": batch.id,
                        "quantity": deduct_qty,
                        "expiry_date": batch.expiry_date.isoformat(),
                    }
                )
                batches_to_update.append(batch)
                remaining_qty -= deduct_qty

            if remaining_qty > 0:
                raise ValueError(
                    f"Insufficient stock for "
                    f"{package_type.medicine.name} "
                    f"({item_data['package_type']})"
                )
            item = BillItem(
                bill=bill,
                medicine=package_type.medicine,
                package_type=item_data["package_type"],
                quantity=item_data["quantity"],
                unit_price=package_type.price,
                total_price=item_data["quantity"] * package_type.price,
                batches_used=batches_used,
            )
            bill_items.append(item)
            total_amount += item.total_price

        BillItem.objects.bulk_create(bill_items)

        if batches_to_update:
            Batch.objects.bulk_update(batches_to_update, ["quantity"])

        bill.total_amount = total_amount
        bill.save()
        return bill
