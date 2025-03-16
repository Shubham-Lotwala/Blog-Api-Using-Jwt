from rest_framework import serializers
from .models import *


# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "country", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            country=validated_data["country"],
            password=validated_data["password"],
        )
        return user


# Serializer for Blog model
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("id", "author", "title", "content", "image", "created_at")
        read_only_fields = ("author",)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Remove the image key if no image is provided
        if not rep.get("image"):
            rep.pop("image", None)
        return rep


# Serializer for Password Reset (Requesting a reset link)
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


# Serializer for Password Reset Confirmation (Setting a new password)
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
