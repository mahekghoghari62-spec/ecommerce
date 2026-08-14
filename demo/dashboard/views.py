import datetime
from decimal import Decimal
from crud.models import Company, Contact, Project, Task
from crud.models import Order as CrudOrder, Product as CrudProduct, Warehouse as CrudWarehouse, Payment as CrudPayment, DailyMetric
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from crud.models import Company, Contact, Project, Task
from crud.models import Order as CrudOrder, Product as CrudProduct, DailyMetric
class NativeContactForm(forms.ModelForm):
    """A deliberately plain ModelForm — no widget attrs, no crispy helper.

    The Bootstrap markup on /native/form comes entirely from the package's
    AdminLTEFormRenderer (FORM_RENDERER in settings) rendering {{ form }}.
    """

    subscribed = forms.BooleanField(required=False, help_text="Get product updates by email.")

    class Meta:
        model = Contact
        fields = ["name", "email", "role", "status", "company"]


def native_form(request):
    """Renderer showcase: plain {{ form }} (validates only; nothing is saved)."""
    form = NativeContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Valid! (Demo only — nothing was saved.)")
        return redirect("native_form")
    return render(request, "showcase/native/form.html", {"form": form})

def dashboard_activity(request):
    """JSON for the Dashboard v1 area chart: six months of orders placed and
    payments completed (by month), aggregated in the database."""
    today = datetime.date.today()
    total = today.year * 12 + today.month - 1
    months = [
        datetime.date((total - offset) // 12, (total - offset) % 12 + 1, 1)
        for offset in range(5, -1, -1)
    ]

    def per_month(queryset, date_field):
        rows = (
            queryset.filter(**{f"{date_field}__gte": months[0]})
            .annotate(month=TruncMonth(date_field))
            .values("month")
            .annotate(count=Count("id"))
        )
        counts = {row["month"]: row["count"] for row in rows}
        return [counts.get(month, 0) for month in months]

    return JsonResponse(
        {
            "categories": [month.isoformat() for month in months],
            "series": [
                {"name": "Orders placed", "data": per_month(CrudOrder.objects, "order_date")},
                {"name": "Payments completed", "data": per_month(CrudPayment.objects.filter(status="completed"), "payment_date")},
            ],
        }
    )

def index(request):
    """Dashboard v1 — small boxes ecommerce data thi (crud app), demo's
    real relational dataset (``manage.py seed_demo``) parthi."""
    stats = {
        "total_orders": CrudOrder.objects.count(),
        "pending_orders": CrudOrder.objects.filter(status="pending").count(),
        "total_products": CrudProduct.objects.count(),
        "total_customers": CrudOrder.objects.values("customer_name").distinct().count(),
    }
    return render(request, "showcase/index.html", {"stats": stats})


def native_demo(request):
    """Phase 2 showcase: Django messages -> AdminLTE alerts + the pagination partial."""
    rows = [
        {"id": i, "name": f"Record {i:03d}", "status": ["Active", "Pending", "Disabled"][i % 3]}
        for i in range(1, 48)
    ]
    page_obj = Paginator(rows, 10).get_page(request.GET.get("page"))
    level = request.GET.get("notify")
    if level == "success":
        messages.success(request, "Saved! This alert is rendered by the AdminLTE messages partial.")
    elif level == "warning":
        messages.warning(request, "Heads up — this is a warning message.")
    elif level == "error":
        messages.error(request, "Something went wrong (error → Bootstrap 'danger').")
    elif level == "info":
        messages.info(request, "Just so you know — an informational message.")
    return render(request, "showcase/native/messages-pagination.html", {"page_obj": page_obj})


def make_page_view(template_name):
    """Return a view that renders the given showcase template.

    The 1:1 page markup lives in the template; no per-page Python is needed.
    """

    def view(request):
        return render(request, template_name)

    view.__name__ = "page_" + template_name.replace("/", "_").replace(".html", "")
    return view


def components_v2(request):
    """Showcase page for the V2 (Tool + extra Widget) components."""
    ctx = {
        "chart_series": [{"name": "Sales", "data": [30, 40, 35, 50, 49, 60, 70]}],
        "chart_categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "dt_columns": [
            {"title": "Name", "field": "name"},
            {"title": "Role", "field": "role"},
            {"title": "Status", "field": "status"},
        ],
        "dt_data": [
            {"name": "Alpha", "role": "Admin", "status": "Active"},
            {"name": "Bravo", "role": "Editor", "status": "Pending"},
            {"name": "Charlie", "role": "Viewer", "status": "Disabled"},
            {"name": "Delta", "role": "Admin", "status": "Active"},
        ],
        "dt_options": {"layout": "fitColumns", "pagination": "local", "paginationSize": 5},
        "tabs": [
            {"title": "Overview", "icon": "bi bi-house", "content": "<p>Overview pane rendered by <code>adminlte_tabs</code>.</p>", "active": True},
            {"title": "Profile", "icon": "bi bi-person", "content": "<p>Profile pane content.</p>"},
            {"title": "Settings", "icon": "bi bi-gear", "content": "<p>Settings pane content.</p>"},
        ],
        "accordion": [
            {"title": "What is AdminLTE 4?", "content": "A Bootstrap 5 admin dashboard template.", "expanded": True},
            {"title": "Is it responsive?", "content": "Yes — it adapts from mobile to desktop."},
            {"title": "Can I customize it?", "content": "Override SCSS variables or the config dict."},
        ],
        "chat": [
            {"message": "Is this template up to date?", "avatar": "/static/adminlte/img/user1-128x128.jpg", "name": "Alexander", "time": "2:30"},
            {"message": "Yes — AdminLTE 4, Bootstrap 5.3.", "is_own": True, "avatar": "/static/adminlte/img/user3-128x128.jpg", "name": "You", "time": "2:31"},
        ],
    }
    return render(request, "showcase/components.html", ctx)


def index3(request):
    """Dashboard v3 — Online Store Overview, wired to real `crud` app data."""
    now = timezone.now()
    today = now.date()

    # ---------- Visitors (last 7 days vs previous 7 days) ----------
    week_start = today - datetime.timedelta(days=6)
    prev_week_start = week_start - datetime.timedelta(days=7)
    prev_week_end = week_start - datetime.timedelta(days=1)

    visitors_this_week = DailyMetric.objects.filter(date__gte=week_start).aggregate(
        total=Sum("total_views")
    )["total"] or 0
    visitors_last_week = DailyMetric.objects.filter(
        date__gte=prev_week_start, date__lte=prev_week_end
    ).aggregate(total=Sum("total_views"))["total"] or 0

    visitors_change_pct = (
        round((visitors_this_week - visitors_last_week) * 100 / visitors_last_week, 1)
        if visitors_last_week else 0
    )

    visitor_days = [week_start + datetime.timedelta(days=i) for i in range(7)]
    visits_map = {
        row["date"]: row["total_views"]
        for row in DailyMetric.objects.filter(date__gte=week_start).values("date", "total_views")
    }
    visitors_series_this_week = [visits_map.get(day, 0) for day in visitor_days]

    prev_visitor_days = [prev_week_start + datetime.timedelta(days=i) for i in range(7)]
    prev_visits_map = {
        row["date"]: row["total_views"]
        for row in DailyMetric.objects.filter(
            date__gte=prev_week_start, date__lte=prev_week_end
        ).values("date", "total_views")
    }
    visitors_series_last_week = [prev_visits_map.get(day, 0) for day in prev_visitor_days]

    # ---------- Sales (this year vs last year) ----------
    sales_this_year = CrudOrder.objects.filter(
        order_date__year=today.year
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    sales_last_year = CrudOrder.objects.filter(
        order_date__year=today.year - 1
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    sales_change_pct = (
        round(float(sales_this_year - sales_last_year) * 100 / float(sales_last_year), 1)
        if sales_last_year else 0
    )

    monthly_sales = (
        CrudOrder.objects.filter(order_date__year=today.year)
        .annotate(month=TruncMonth("order_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    sales_categories = [row["month"].strftime("%b") for row in monthly_sales]
    sales_values = [float(row["total"]) for row in monthly_sales]

    # ---------- Top products by units sold ----------
    top_products = (
        CrudOrder.objects.values("product__id", "product__name", "product__price")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:4]
    )

    # ---------- Simple overview rates ----------
    total_orders = CrudOrder.objects.count()
    total_customers = CrudOrder.objects.values("customer_name").distinct().count()
    total_visitors_ever = DailyMetric.objects.aggregate(total=Sum("total_views"))["total"] or 0

    conversion_rate = round(total_orders * 100 / total_visitors_ever, 1) if total_visitors_ever else 0

    context = {
        "visitors_total": visitors_this_week,
        "visitors_change_pct": visitors_change_pct,
        "visitors_categories": [d.strftime("%d") + "th" for d in visitor_days],
        "visitors_series_this_week": visitors_series_this_week,
        "visitors_series_last_week": visitors_series_last_week,

        "sales_total": sales_this_year,
        "sales_change_pct": sales_change_pct,
        "sales_categories": sales_categories,
        "sales_values": sales_values,

        "top_products": top_products,

        "conversion_rate": conversion_rate,
        "total_orders": total_orders,
        "total_customers": total_customers,
    }
    return render(request, "showcase/index3.html", context)
# Country name -> ISO2 code, jsVectorMap 'world' region keys માટે.
# List ma tamara data ma je countries hoy e badha add karo — jo naam
# ahi map ma na hoy to e country map par count nahi thay.
COUNTRY_NAME_TO_ISO2 = {
    "India": "IN", "United States": "US", "USA": "US", "United Kingdom": "GB",
    "UK": "GB", "Canada": "CA", "Australia": "AU", "Germany": "DE", "France": "FR",
    "China": "CN", "Japan": "JP", "Brazil": "BR", "Russia": "RU",
    "South Africa": "ZA", "UAE": "AE", "United Arab Emirates": "AE",
    "Singapore": "SG", "Nepal": "NP", "Bangladesh": "BD", "Sri Lanka": "LK",
    "Pakistan": "PK", "Italy": "IT", "Spain": "ES", "Netherlands": "NL",
    "Mexico": "MX", "Indonesia": "ID", "Malaysia": "MY", "Thailand": "TH",
    "South Korea": "KR", "Saudi Arabia": "SA", "New Zealand": "NZ",
}


def dashboard_sales_widget(request):
    """JSON for the Sales Value card: world map (orders by country) +
    3 sparklines — Visitors (DailyMetric.total_views), Online (daily
    completed payments count), Sales (daily order count)."""
    today = timezone.now().date()
    days = [today - datetime.timedelta(days=i) for i in range(8, -1, -1)]  # last 9 days

    # ---- World map: order count by country ----
    country_counts = (
        CrudOrder.objects.exclude(country__isnull=True)
        .exclude(country__exact="")
        .values("country")
        .annotate(count=Count("id"))
    )
    map_values = {}
    for row in country_counts:
        iso = COUNTRY_NAME_TO_ISO2.get(row["country"])
        if iso:
            map_values[iso] = map_values.get(iso, 0) + row["count"]

    # ---- Sparkline 1: Visitors ----
    visits_rows = DailyMetric.objects.filter(date__gte=days[0]).values("date", "total_views")
    visits_map = {row["date"]: row["total_views"] for row in visits_rows}
    sparkline_visitors = [visits_map.get(d, 0) for d in days]

    # ---- Sparkline 2: Online = completed payments per day ----
    payment_rows = (
        CrudPayment.objects.filter(status="completed", payment_date__gte=days[0])
        .annotate(day=TruncDate("payment_date"))
        .values("day")
        .annotate(count=Count("id"))
    )
    payments_map = {row["day"]: row["count"] for row in payment_rows}
    sparkline_online = [payments_map.get(d, 0) for d in days]

    # ---- Sparkline 3: Sales = orders per day ----
    order_rows = (
        CrudOrder.objects.filter(order_date__gte=days[0])
        .annotate(day=TruncDate("order_date"))
        .values("day")
        .annotate(count=Count("id"))
    )
    orders_map = {row["day"]: row["count"] for row in order_rows}
    sparkline_sales = [orders_map.get(d, 0) for d in days]

    return JsonResponse(
        {
            "map_values": map_values,
            "sparkline_visitors": sparkline_visitors,
            "sparkline_online": sparkline_online,
            "sparkline_sales": sparkline_sales,
        }
    )