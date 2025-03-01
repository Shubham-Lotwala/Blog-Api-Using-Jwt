from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import (
    register_user,
    login_user,
    logout_user,
    blog_list,
    blog_detail,
    forgot_password,
    reset_password,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", register_user, name="register"),
    path("api/login/", login_user, name="login"),
    path("api/logout/", logout_user, name="logout"),
    path("api/blogs/", blog_list, name="blog-list"),
    path("api/blogs/<int:pk>/", blog_detail, name="blog-detail"),
    path("api/forgot-password/", forgot_password, name="forgot-password"),
    path("api/reset-password/<str:token>/", reset_password, name="reset-password"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
