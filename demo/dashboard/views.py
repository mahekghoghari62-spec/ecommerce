import datetime
from decimal import Decimal

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from crud.models import Company, Contact, Project, Task
from shop.models import Order, OrderItem, SiteVisit


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


def index(request):
    """Dashboard v1 — the small boxes and the activity chart are fed by the
    demo's own relational dataset (``manage.py seed_demo``), not static markup."""
    tasks_total = Task.objects.count()
    tasks_done = Task.objects.filter(status="done").count()
    stats = {
        "projects_active": Project.objects.filter(status="active").count(),
        "tasks_done_pct": round(tasks_done * 100 / tasks_total) if tasks_total else 0,
        "contacts": Contact.objects.count(),
        "companies": Company.objects.count(),
    }
    return render(request, "showcase/index.html", {"stats": stats})


def dashboard_activity(request):
    """JSON for the Dashboard v1 area chart: six months of projects started and
    tasks completed (by due month), aggregated in the database."""
    today = datetime.date.today()
    # Calendar month arithmetic — stepping by timedelta(days=31) skips or
    # duplicates months depending on the current date.
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
                {"name": "Projects started", "data": per_month(Project.objects, "start_date")},
                {"name": "Tasks completed", "data": per_month(Task.objects.filter(status="done"), "due_date")},
            ],
        }
    )


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
    """Dashboard v3 — Online Store Overview, wired to real `shop` app data."""
    now = timezone.now()
    today = now.date()

    # ---------- Visitors (last 7 days vs previous 7 days) ----------
    week_start = today - datetime.timedelta(days=6)
    prev_week_start = week_start - datetime.timedelta(days=7)
    prev_week_end = week_start - datetime.timedelta(days=1)

    visitors_this_week = SiteVisit.objects.filter(visited_at__date__gte=week_start).count()
    visitors_last_week = SiteVisit.objects.filter(
        visited_at__date__gte=prev_week_start, visited_at__date__lte=prev_week_end
    ).count()

    visitors_change_pct = (
        round((visitors_this_week - visitors_last_week) * 100 / visitors_last_week, 1)
        if visitors_last_week else 0
    )

    # Daily visitor counts for the last 7 days (for the line chart)
    visitor_days = [week_start + datetime.timedelta(days=i) for i in range(7)]
    visits_by_day = (
        SiteVisit.objects.filter(visited_at__date__gte=week_start)
        .annotate(day=TruncDate("visited_at"))
        .values("day")
        .annotate(count=Count("id"))
    )
    visits_map = {row["day"]: row["count"] for row in visits_by_day}
    visitors_series_this_week = [visits_map.get(day, 0) for day in visitor_days]

    prev_visitor_days = [prev_week_start + datetime.timedelta(days=i) for i in range(7)]
    prev_visits_by_day = (
        SiteVisit.objects.filter(visited_at__date__gte=prev_week_start, visited_at__date__lte=prev_week_end)
        .annotate(day=TruncDate("visited_at"))
        .values("day")
        .annotate(count=Count("id"))
    )
    prev_visits_map = {row["day"]: row["count"] for row in prev_visits_by_day}
    visitors_series_last_week = [prev_visits_map.get(day, 0) for day in prev_visitor_days]

    # ---------- Sales (this year vs last year) ----------
    sales_this_year = Order.objects.filter(
        created_at__year=today.year
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    sales_last_year = Order.objects.filter(
        created_at__year=today.year - 1
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    sales_change_pct = (
        round(float(sales_this_year - sales_last_year) * 100 / float(sales_last_year), 1)
        if sales_last_year else 0
    )

    # Monthly sales for the current year (for the bar chart)
    monthly_sales = (
        Order.objects.filter(created_at__year=today.year)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )
    sales_categories = [row["month"].strftime("%b") for row in monthly_sales]
    sales_values = [float(row["total"]) for row in monthly_sales]

    # ---------- Top products by units sold ----------
    top_products = (
        OrderItem.objects.values("product__id", "product__name", "product__price")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:4]
    )

    # ---------- Simple overview rates ----------
    total_orders = Order.objects.count()
    total_customers = Order.objects.values("customer").distinct().count()
    total_visitors_ever = SiteVisit.objects.count()

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