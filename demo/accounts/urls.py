from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import AdminLoginForm

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            # Demo login page: extends the package auth card, pre-fills the seeded
            # credentials and explains the demo layout.
            template_name="accounts/login.html",
            authentication_form=AdminLoginForm,
            # Keep the form available so a shop user can switch to an admin account.
            redirect_authenticated_user=False,
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("lockscreen/", views.lockscreen, name="lockscreen"),
    # Built-in password change + reset flow (AdminLTE-themed registration/* templates).
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path(
    'password_reset/',
    auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html',
    ),
    name='password_reset',
),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
