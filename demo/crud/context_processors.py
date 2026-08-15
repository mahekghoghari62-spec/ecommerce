from copy import deepcopy
from django.conf import settings
from django.urls import reverse


def dynamic_usermenu(request):
    """Overrides the static ADMINLTE usermenu with the logged-in user's info."""
    adminlte = deepcopy(getattr(settings, "ADMINLTE", {}))

    if request.user.is_authenticated:
        full_name = request.user.get_full_name() or request.user.username
        usermenu = adminlte.get("usermenu", {})
        usermenu["name"] = full_name
        usermenu["description"] = "Staff" if request.user.is_staff else "User"
        usermenu["since"] = f"Member since {request.user.date_joined.strftime('%b. %Y')}"
        usermenu["stats"] = [
            {"label": "Settings", "url": reverse("crud:settings")},
        ]
        adminlte["usermenu"] = usermenu

    return {"adminlte": adminlte}