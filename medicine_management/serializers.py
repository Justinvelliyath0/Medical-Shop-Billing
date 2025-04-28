from django.db import transaction
from django.db.models import Prefetch
from rest_framework import serializers
from medicine_management.models import Medicine, PackageTypes, Batch


class BatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Batch
        fields = ("id", "quantity", "expiry_date", "purchase_date")


class PackageTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    batches = BatchSerializer(many=True)

    class Meta:
        model = PackageTypes
        fields = ("id", "package_type", "price", "batches")


class MedicineSerializer(serializers.ModelSerializer):
    package_types = PackageTypeSerializer(many=True)

    class Meta:
        model = Medicine
        fields = "__all__"

    def create(self, validated_data):
        packages = validated_data.pop("package_types")
        with transaction.atomic():
            medicine = Medicine.objects.create(**validated_data)
            for package in packages:
                batches = package.pop("batches")
                package_type = PackageTypes.objects.create(
                    medicine=medicine, **package
                )
                for batch in batches:
                    Batch.objects.create(package_type=package_type, **batch)
        return medicine

    @staticmethod
    def setup_eager_loading(queryset):
        """Prefetch all related data"""
        return queryset.prefetch_related(
            Prefetch(
                "package_types",
                queryset=PackageTypes.objects.all().prefetch_related(
                    Prefetch("batches", queryset=Batch.objects.all())
                ),
            )
        )

    def update(self, instance, validated_data):
        package_types_data = validated_data.pop("package_types", [])
        existing_packages = {p.id: p for p in instance.package_types.all()}

        with transaction.atomic():
            # Update medicine
            instance = super().update(instance, validated_data)

            # Process packages
            for package_data in package_types_data:
                package_id = package_data.get("id")
                batches_data = package_data.pop("batches", [])

                if package_id in existing_packages:
                    self._update_package(
                        existing_packages.pop(package_id),
                        package_data,
                        batches_data,
                    )
                else:
                    self._create_package(instance, package_data, batches_data)

            # Delete remaining packages (1 bulk query)
            if existing_packages:
                PackageTypes.objects.filter(
                    id__in=existing_packages.keys()
                ).delete()

        return instance

    @staticmethod
    def _create_package(medicine, package_data, batches_data):
        """Create package with batches (2 queries)"""
        package = PackageTypes.objects.create(
            medicine=medicine, **package_data
        )
        Batch.objects.bulk_create(
            [Batch(package_type=package, **b) for b in batches_data]
        )
        return package

    def _update_package(self, package, package_data, batches_data):
        """Update package and its batches"""
        existing_batches = {b.id: b for b in package.batches.all()}

        # Update package
        for attr, value in package_data.items():
            setattr(package, attr, value)
        package.save()

        # Process batches
        for batch_data in batches_data:
            batch_id = batch_data.get("id")
            if batch_id in existing_batches:
                self._update_batch(existing_batches.pop(batch_id), batch_data)
            else:
                self._create_batch(package, batch_data)

        # Delete remaining batches
        if existing_batches:
            Batch.objects.filter(id__in=existing_batches.keys()).delete()

        return package

    @staticmethod
    def _create_batch(package, batch_data):
        Batch.objects.create(package_type=package, **batch_data)

    @staticmethod
    def _update_batch(batch, batch_data):
        for attr, value in batch_data.items():
            setattr(batch, attr, value)
        batch.save()


class MedicineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ("id", "name", "generic_name", "category")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Initialize all package types with empty strings
        for choice in PackageTypes.PACKAGE_TYPES:
            data[choice[0]] = ""

        # Populate with actual data
        for package in instance.package_types.all():
            stock = sum(batch.quantity for batch in package.batches.all())
            data[package.package_type] = f"{stock} nos (₹{package.price})"

        return data
