"""1:1 sidebar menu + topbar dropdown data, mirroring the AdminLTE 4 HTML demo
(`src/html/components/dashboard/_sidenav-demo.astro` and `_topbar.astro`).

Every internal item uses `route:` (a named URL reversed by HrefFilter) rather
than a hardcoded path — the Django-idiomatic way; active-state detection still
works automatically (ActiveFilter derives patterns from the resolved href)."""

_circle = "bi bi-circle"


def _is_staff(request) -> bool:
    """`can` callables receive the current request (GateFilter)."""
    return request.user.is_staff

ADMINLTE_MENU = [
    {"text": "Dashboard", "route": "index3", "icon": "bi bi-speedometer"},
    {"header": "MANAGE BUSINESS"},
    {"text": "Orders", "route": "crud:order_list", "icon": "bi bi-bag-check"},
    {"text": "Returns", "route": "crud:return_list", "icon": "bi bi-arrow-return-left"},
    {"text": "Pricing", "route": "crud:pricing_list", "icon": "bi bi-tag"},
    {"text": "Claims", "route": "crud:claim_list", "icon": "bi bi-exclamation-triangle"},
    {"text": "Inventory", "route": "crud:inventory_list", "icon": "bi bi-box-seam"},
    {"text": "Catalog Uploads", "route": "crud:catalogupload_list", "icon": "bi bi-cloud-upload"},
    {"text": "Image Bulk Uploads", "route": "crud:imagebulkupload_list", "icon": "bi bi-images"},
    {"text": "Quality", "route": "crud:quality_list", "icon": "bi bi-clipboard-check"},
]

# --- Topbar dropdown data (mirrors _topbar.astro) ---
# Emptied out so the top navbar shows no messages/notifications dropdowns.
NAVBAR_MESSAGES = {
    "count": 0,
    "items": [],
}

NAVBAR_NOTIFICATIONS = {
    "count": 0,
    "items": [],
}

USERMENU = {
    "image": "adminlte/img/user2-160x160.jpg",
    "name": "Alexander Pierce",
    "description": "Web Developer",
    "since": "Member since Nov. 2023",
    "stats": [
        {"label": "Followers", "url": "#"},
        {"label": "Sales", "url": "#"},
        {"label": "Friends", "url": "#"},
    ],
}