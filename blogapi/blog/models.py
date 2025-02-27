from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


# Custom user manager to handle user creation
class CustomUserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, email, first_name, last_name, country, password=None):
        if not email:
            raise ValueError("Email must be set")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not country:
            raise ValueError("Country is required")

        email = self.normalize_email(email)  # Normalize email address
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, country=country
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save user to database
        return user

    # Method to create a superuser (admin)
    def create_superuser(self, email, first_name, last_name, country, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            country=country,
            password=password,
        )
        user.is_staff = True  # Grant admin privileges
        user.is_superuser = True  # Grant superuser privileges
        user.save(using=self._db)
        return user


# Custom user model extending Django's AbstractBaseUser
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Unique email field (acts as username)
    first_name = models.CharField(max_length=30)  # First name of the user
    last_name = models.CharField(max_length=30)  # Last name of the user
    country = models.CharField(max_length=50)  # Country field
    is_staff = models.BooleanField(
        default=False
    )  # Determines if user can access admin panel
    is_active = models.BooleanField(default=True)  # Active status of the user
    date_joined = models.DateTimeField(default=timezone.now)  # Date of account creation

    objects = CustomUserManager()  # Use custom user manager

    USERNAME_FIELD = "email"  # Use email as the username field
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "country",
    ]  # Required fields when creating a user

    def __str__(self):
        return self.email  # String representation of the user


# Blog model to store blog posts
class Blog(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )  # Link blog to user
    title = models.CharField(max_length=200)  # Title of the blog
    content = models.TextField()  # Blog content
    image = models.ImageField(
        upload_to="blog_images/", null=True, blank=True
    )  # Optional image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of blog creation

    def __str__(self):
        return self.title  # String representation of the blog post


# Model to store password reset tokens
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link token to user
    token = models.CharField(
        max_length=100, unique=True
    )  # Unique token for password reset
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of token creation
    expires_at = models.DateTimeField()  # Expiration time for the token

    def __str__(self):
        return f"Token for {self.user.email}"  # String representation of the token
