from rest_framework import serializers
from .models import CustomUser, Blog


# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  # Password field should be write-only

    class Meta:
        model = CustomUser  # Linking to the CustomUser model
        fields = (
            "email",
            "first_name",
            "last_name",
            "country",
            "password",
        )  # Defining fields to be serialized
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Ensure password is never read back in responses

    def create(self, validated_data):
        # Creating a user using the create_user method (assumes CustomUser has create_user method)
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
        model = Blog  # Linking to the Blog model
        fields = (
            "id",
            "author",
            "title",
            "content",
            "image",
            "created_at",
        )  # Defining fields to be serialized
        read_only_fields = (
            "author",
        )  # Ensuring author field cannot be modified via the API


# Serializer for Password Reset (Requesting a reset link)
class PasswordResetSerializer(serializers.Serializer):
    email = (
        serializers.EmailField()
    )  # Email field to identify the user requesting a reset


# Serializer for Password Reset Confirmation (Setting a new password)
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8
    )  # Ensuring a minimum password length
