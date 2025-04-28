import re

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_deleted:
            raise serializers.ValidationError("Account is deactivated")

        data.update(
            {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "role": user.role,
            }
        )
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "name",
            "role",
            "created_by",
        ]

    def validate_password(self, value):
        pattern = re.compile(r"^(?=.*[a-zA-Z])(?=.*\d).{6,}$")
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Password must contain at least one letter, "
                "one digit, and be at least 6 characters long."
            )
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "password and confirm_password don't match"
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)
