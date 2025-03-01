from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
import secrets
from .models import Blog, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer,
    BlogSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)

CustomUser = get_user_model()


# User Registration View
@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User Registration Successful", "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View
@api_view(["POST"])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = CustomUser.objects.filter(email=email).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
    )


# User Logout View
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    return Response(
        {"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT
    )


# Blog List and Creation View
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def blog_list(request):
    if request.method == "GET":
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Blog Detail, Update, and Delete View
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"message": "No Blog Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    elif request.method in ["PUT", "DELETE"]:
        if blog.author != request.user:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.method == "PUT":
            # Allow partial updates (e.g. updating the image without changing other fields)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            blog.delete()
            return Response(
                {"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT
            )


# Forgot Password View
@api_view(["POST"])
def forgot_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User with this email does not exist."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate a password reset token
    token = secrets.token_urlsafe(32)
    expires_at = timezone.now() + timezone.timedelta(hours=1)

    # Save the token in the database
    PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

    # Generate a reset link
    reset_link = f"http://localhost:8000/api/reset-password/{token}/"

    # Send reset link via email
    send_mail(
        "Password Reset Request",
        f"Click the link to reset your password: {reset_link}",
        "noreply@blogapi.com",
        [user.email],
        fail_silently=False,
    )

    return Response(
        {"message": "Password reset link has been sent to your email."},
        status=status.HTTP_200_OK,
    )


# Reset Password View
@api_view(["POST"])
def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if token has expired
    if timezone.now() > reset_token.expires_at:
        reset_token.delete()
        return Response(
            {"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = PasswordResetConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Reset user password
    user = reset_token.user
    user.set_password(serializer.validated_data["new_password"])
    user.save()

    # Delete the used token
    reset_token.delete()

    return Response(
        {"message": "Password has been reset successfully."}, status=status.HTTP_200_OK
    )
