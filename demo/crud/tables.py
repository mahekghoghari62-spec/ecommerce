import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import CatalogUpload, Claim, Contact, ImageBulkUpload, Inventory, Order, Pricing, Project, Product, Quality, Return

_PROJECT_STATUS_CLASS = {
    "planning": "info", "active": "success", "on_hold": "warning", "completed": "secondary",
}
_ORDER_STATUS_CLASS = {
    "pending": "warning", "processing": "info", "shipped": "primary",
    "delivered": "success", "cancelled": "danger",
}
_RETURN_STATUS_CLASS = {
    "requested": "warning", "approved": "info", "rejected": "danger",
    "picked_up": "primary", "refunded": "success",
}
_PRICING_STATUS_CLASS = {"active": "success", "draft": "warning", "archived": "secondary"}
_CLAIM_STATUS_CLASS = {
    "open": "warning", "under_review": "info", "approved": "primary",
    "rejected": "danger", "settled": "success",
}
_INVENTORY_STATUS_CLASS = {
    "in_stock": "success", "low_stock": "warning",
    "out_of_stock": "danger", "discontinued": "secondary",
}
_CATALOG_STATUS_CLASS = {
    "pending": "warning", "processing": "info",
    "completed": "success", "failed": "danger",
}
_IMAGE_BULK_STATUS_CLASS = {
    "pending": "warning", "processing": "info",
    "completed": "success", "failed": "danger",
}
_QUALITY_STATUS_CLASS = {
    "pending": "warning", "passed": "success",
    "failed": "danger", "rework": "info",
}
_STATUS_CLASS = {"active": "success", "pending": "warning", "disabled": "secondary"}


class OrderTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="crud/_order_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Order
        fields = ("order_number", "customer_name", "product", "quantity", "amount", "status", "order_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-order_date"

    def render_status(self, record):
        cls = _ORDER_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_amount(self, value):
        return format_html("${}", f"{value:,.2f}")


class ContactTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="crud/_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Contact
        fields = ("name", "email", "company", "role", "status", "created")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = _STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_role(self, record):
        return record.get_role_display()


class ProjectTable(tables.Table):
    name = tables.Column(linkify=True)
    team = tables.Column(verbose_name="Team", orderable=False, empty_values=())

    class Meta:
        model = Project
        fields = ("name", "company", "status", "budget", "start_date", "due_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-start_date"

    def render_status(self, record):
        cls = _PROJECT_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_budget(self, value):
        return format_html("${}", f"{value:,.0f}")

    def render_team(self, record):
        return format_html('<span class="badge text-bg-light text-dark">{} members</span>', record.team.count())


class ReturnTable(tables.Table):
    order = tables.Column(linkify=True, verbose_name="Order #")
    actions = tables.TemplateColumn(
        template_name="crud/_return_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Return
        fields = ("order", "reason", "status", "requested_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-requested_date"

    def render_status(self, record):
        cls = _RETURN_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_reason(self, record):
        return record.get_reason_display()


class PricingTable(tables.Table):
    product = tables.Column(linkify=True)
    final_price = tables.Column(verbose_name="Final Price", orderable=False, empty_values=())
    margin_percent = tables.Column(verbose_name="Margin %", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_pricing_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Pricing
        fields = ("product", "cost_price", "selling_price", "discount_percent", "status", "effective_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-effective_date"

    def render_status(self, record):
        cls = _PRICING_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_cost_price(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_selling_price(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_final_price(self, record):
        return format_html("${}", f"{record.final_price:,.2f}")

    def render_margin_percent(self, record):
        return format_html("{}%", record.margin_percent)

    def render_discount_percent(self, value):
        return format_html("{}%", value)


class ClaimTable(tables.Table):
    order = tables.Column(linkify=True, verbose_name="Order #")
    actions = tables.TemplateColumn(
        template_name="crud/_claim_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Claim
        fields = ("order", "claim_type", "status", "claim_amount", "filed_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-filed_date"

    def render_status(self, record):
        cls = _CLAIM_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_claim_type(self, record):
        return record.get_claim_type_display()

    def render_claim_amount(self, value):
        return format_html("${}", f"{value:,.2f}")


class InventoryTable(tables.Table):
    product = tables.Column(linkify=True)
    actions = tables.TemplateColumn(
        template_name="crud/_inventory_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Inventory
        fields = ("product", "quantity", "reorder_level", "warehouse_location", "status", "last_restocked")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "product__name"

    def render_status(self, record):
        cls = _INVENTORY_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_quantity(self, record):
        if record.is_low:
            return format_html('<span class="text-danger fw-bold">{}</span>', record.quantity)
        return record.quantity


class CatalogUploadTable(tables.Table):
    file_name = tables.Column(linkify=True)
    success_rate = tables.Column(verbose_name="Success %", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_catalog_upload_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = CatalogUpload
        fields = ("file_name", "status", "total_rows", "processed_rows", "error_count", "uploaded_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-uploaded_date"

    def render_status(self, record):
        cls = _CATALOG_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_success_rate(self, record):
        return format_html("{}%", record.success_rate)

    def render_error_count(self, value):
        if value > 0:
            return format_html('<span class="text-danger fw-bold">{}</span>', value)
        return value


class ImageBulkUploadTable(tables.Table):
    name = tables.Column(linkify=True)
    success_rate = tables.Column(verbose_name="Success %", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_image_bulk_upload_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = ImageBulkUpload
        fields = ("name", "status", "total_images", "processed_images", "error_count", "uploaded_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-uploaded_date"

    def render_status(self, record):
        cls = _IMAGE_BULK_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_success_rate(self, record):
        return format_html("{}%", record.success_rate)

    def render_error_count(self, value):
        if value > 0:
            return format_html('<span class="text-danger fw-bold">{}</span>', value)
        return value


class QualityTable(tables.Table):
    product = tables.Column(linkify=True)
    actions = tables.TemplateColumn(
        template_name="crud/_quality_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Quality
        fields = ("product", "batch_number", "inspector_name", "status", "defect_count", "inspection_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-inspection_date"

    def render_status(self, record):
        cls = _QUALITY_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_defect_count(self, record):
        if record.defect_count > 0:
            return format_html('<span class="text-danger fw-bold">{}</span>', record.defect_count)
        return record.defect_count


class ProductTable(tables.Table):
    name = tables.Column(linkify=True)
    image = tables.Column(orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_product_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Product
        fields = ("name", "category", "price", "status")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = {"active": "success", "draft": "warning", "inactive": "secondary"}.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_category(self, record):
        return record.get_category_display()

    def render_price(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_image(self, record):
        if record.image:
            return format_html('<img src="{}" style="width:36px;height:36px;object-fit:cover;border-radius:6px;">', record.image.url)
        return mark_safe('<span class="text-muted">—</span>')