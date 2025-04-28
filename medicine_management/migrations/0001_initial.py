import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Medicine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("generic_name", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("painkiller", "Painkiller"),
                            ("antibiotic", "Antibiotic"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "medicines",
            },
        ),
        migrations.CreateModel(
            name="PackageTypes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "package_type",
                    models.CharField(
                        choices=[
                            ("single", "Single Piece/Strip"),
                            ("pack", "Pack"),
                            ("box", "Box"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medicine_management.medicine",
                    ),
                ),
            ],
            options={
                "db_table": "medicine_package_type",
            },
        ),
        migrations.CreateModel(
            name="Batch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("expiry_date", models.DateField()),
                ("purchase_date", models.DateField()),
                (
                    "package_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medicine_management.packagetypes",
                    ),
                ),
            ],
            options={
                "db_table": "medicine_batch",
            },
        ),
        migrations.AddIndex(
            model_name="medicine",
            index=models.Index(
                fields=["name", "generic_name"],
                name="medicines_name_82a235_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="packagetypes",
            unique_together={("medicine", "package_type")},
        ),
        migrations.AddIndex(
            model_name="batch",
            index=models.Index(
                fields=["expiry_date"], name="medicine_ba_expiry__92678e_idx"
            ),
        ),
    ]
