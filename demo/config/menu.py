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
    {
    "text": "Orders",
    "icon": "bi bi-bag-check",
    "submenu": [
        {"text": "Manage Orders", "route": "crud:order_list", "icon": "bi bi-circle"},
    ],
    },
    {"text": "Returns", "route": "crud:return_list", "icon": "bi bi-arrow-return-left"},
    {
    "text": "Pricing",
    "icon": "bi bi-tag",
    "submenu": [
        {"text": "Manage Pricing", "route": "crud:pricing_list", "active": ["pricing"]},
        {"text": "Reduce RTOs & Returns", "route": "crud:reduce_rto_returns"},
    ],
},
    {"text": "Claims", "route": "crud:claim_list", "icon": "bi bi-exclamation-triangle"},
    {"text": "Inventory", "route": "crud:inventory_list", "icon": "bi bi-box-seam"},
    {"text": "Catalog Uploads", "route": "crud:catalogupload_list", "icon": "bi bi-cloud-upload"},
    {"text": "Image Bulk Uploads", "route": "crud:imagebulkupload_list", "icon": "bi bi-images"},
    {"text": "Quality", "route": "crud:quality_list", "icon": "bi bi-clipboard-check"},
    {"text": "Products", "route": "crud:product_list", "icon": "bi bi-box"},
    {"text": "Payments", "route": "crud:payment_list", "icon": "bi bi-credit-card"},
    {"text": "Warehouse", "route": "crud:warehouse_list", "icon": "bi bi-building"},
    {"header": "BOOST SALES"},
    {"text": "Influencer Campaigns", "route": "crud:influencercampaign_list", "icon": "bi bi-person-badge"},
    {"text": "Advertisement", "route": "crud:advertisement_list", "icon": "bi bi-megaphone"},

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