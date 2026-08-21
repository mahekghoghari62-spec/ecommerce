from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class AdminLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff or (not user.is_superuser and not hasattr(user, "panel_profile")):
            raise forms.ValidationError(
                "This login is only for admin panel users.",
                code="admin_login_required",
            )
        if hasattr(user, "panel_profile") and user.panel_profile.status != "active":
            raise forms.ValidationError(
                "This admin panel user is inactive.",
                code="inactive_panel_user",
            )


class CustomerLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff:
            raise forms.ValidationError(
                "This login is only for shop users.",
                code="customer_login_required",
            )
