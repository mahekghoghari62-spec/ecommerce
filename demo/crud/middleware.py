from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """Redirect anonymous users to the login page for every URL except a
    small allow-list (login itself, password reset, register, static/media,
    and the Django admin login).
    """

    # URL path prefixes that stay accessible without logging in.
    EXEMPT_PREFIXES = [
        "/login",
        "/logout",
        "/password_reset",
        "/reset",
        "/register",
        "/accounts/",
        "/admin/login",
        "/static/",
        "/media/",
        "/favicon.ico",
        "/shop/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        is_exempt = any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES)

        if not request.user.is_authenticated and not is_exempt:
            login_url = getattr(settings, "LOGIN_URL", "/login/")
            return redirect(f"{login_url}?next={path}")

        return self.get_response(request)