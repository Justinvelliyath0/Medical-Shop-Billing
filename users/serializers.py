import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "role"]


class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        write_only=True, required=False, min_length=6
    )
    confirm_password = serializers.CharField(
        write_only=True, required=False, min_length=6
    )

    class Meta:
        model = User
        fields = ("name", "role", "username", "password", "confirm_password")

    def validate_password(self, value):
        if value:
            pattern = re.compile(r"^(?=.*[a-zA-Z])(?=.*\d).{6,}$")
            if not pattern.match(value):
                raise serializers.ValidationError(
                    "Password must contain at least one letter, "
                    "one digit, and be at least 6 characters long."
                )
        return value

    def validate(self, data):
        # Ensure password and confirm_password match
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password and not confirm_password:
            raise serializers.ValidationError("Please enter confirm_password.")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(
                "Password and confirm password do not match."
            )
        if password:
            data["password"] = make_password(password)
        return data
