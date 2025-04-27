from django.db import migrations
from django.contrib.auth.hashers import make_password
from decouple import config


def create_first_admin(apps, schema_editor):
    User = apps.get_model("users", "User")
    username = config("ADMIN_USERNAME", default="Admin")
    password = make_password(config("ADMIN_PASSWORD", default="Admin@123"))
    User.objects.create(
        username=username,
        password=password,
        name="Admin",
        role="ADMIN",
        is_superuser=True,
        created_by=None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_first_admin)]
