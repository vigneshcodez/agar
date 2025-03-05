from django.urls import path
from .views import register, activate, user_login, user_logout, password_reset_request, password_reset_confirm

urlpatterns = [
    path("register/", register, name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("password-reset/", password_reset_request, name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm"),
]
