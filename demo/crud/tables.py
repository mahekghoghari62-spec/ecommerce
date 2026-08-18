import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Advertisement, CatalogUpload, Claim, Contact, ImageBulkUpload, InfluencerCampaign, Inventory, Order,Payment,PanelUser, Pricing, Project, Product,Promotion, Quality, Return, Warehouse
DATETIME_FMT = "d/m/Y, h:i A"
DATE_FMT = "d/m/Y"
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
_WAREHOUSE_STATUS_CLASS = {
    "active": "success", "inactive": "secondary", "under_maintenance": "warning",
}

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
        fields = ("product", "quantity", "reorder_level", "warehouse", "status", "last_restocked")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "product__name"

    def render_status(self, record):
        cls = _INVENTORY_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_quantity(self, record):
        if record.is_low:
            return format_html('<span class="text-danger fw-bold">{}</span>', record.quantity)
        return record.quantity


_QC_STATUS_LABEL = {
    "pending": "Action Required",
    "processing": "QC in Progress",
    "completed": "QC Pass",
    "failed": "QC Error",
}
_QC_STATUS_CLASS = {
    "pending": "danger", "processing": "warning",
    "completed": "success", "failed": "danger",
}


class CatalogUploadTable(tables.Table):
    file_name = tables.Column(linkify=True, verbose_name="File Id")
    category = tables.Column(verbose_name="Category")
    success_rate = tables.Column(verbose_name="Success %", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_catalog_upload_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = CatalogUpload
        fields = ("file_name", "category", "status", "total_rows", "processed_rows", "error_count", "uploaded_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-uploaded_date"

    def render_category(self, record):
        return record.get_category_display()

    def render_status(self, record):
        cls = _QC_STATUS_CLASS.get(record.status, "secondary")
        label = _QC_STATUS_LABEL.get(record.status, record.get_status_display())
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, label)

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
    selling_price = tables.Column(verbose_name="Selling Price (incl. GST)", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_product_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Product
        fields = ("name", "category", "price", "gst_percent", "selling_price", "status")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = {"active": "success", "draft": "warning", "inactive": "secondary"}.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_category(self, record):
        return record.get_category_display()

    def render_price(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_gst_percent(self, value):
        return f"{value}%"

    def render_selling_price(self, record):
        return format_html("${}", f"{record.selling_price:,.2f}")

    def render_image(self, record):
        if record.image:
            return format_html('<img src="{}" style="width:36px;height:36px;object-fit:cover;border-radius:6px;">', record.image.url)
        return mark_safe('<span class="text-muted">—</span>')

_PAYMENT_STATUS_CLASS = {
    "pending": "warning", "completed": "success",
    "failed": "danger", "refunded": "secondary",
}


class PaymentTable(tables.Table):
    order = tables.Column(linkify=True, verbose_name="Order #")
    payment_date = tables.DateTimeColumn(format=DATETIME_FMT, verbose_name="Payment Date")
    actions = tables.TemplateColumn(
        template_name="crud/_payment_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Payment
        fields = ("order", "amount", "method", "status", "transaction_id", "payment_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-payment_date"

    def render_status(self, record):
        cls = _PAYMENT_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_method(self, record):
        return record.get_method_display()

    def render_amount(self, value):
        return format_html("${}", f"{value:,.2f}")
class WarehouseTable(tables.Table):
    name = tables.Column(linkify=True)
    actions = tables.TemplateColumn(
        template_name="crud/_warehouse_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Warehouse
        fields = ("name", "location", "capacity", "manager_name", "contact_number", "status")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = _WAREHOUSE_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())
_INFLUENCER_STATUS_CLASS = {
    "planned": "info", "active": "success", "completed": "secondary", "cancelled": "danger",
}


class InfluencerCampaignTable(tables.Table):
    campaign_name = tables.Column(linkify=True)
    product = tables.Column(linkify=True)
    start_date = tables.DateColumn(format=DATE_FMT, verbose_name="Start Date")
    end_date = tables.DateColumn(format=DATE_FMT, verbose_name="End Date")
    actions = tables.TemplateColumn(
        template_name="crud/_influencercampaign_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = InfluencerCampaign
        fields = ("campaign_name", "product", "influencer_name", "platform", "followers", "budget", "status", "start_date", "end_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-start_date"

    def render_status(self, record):
        cls = _INFLUENCER_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_platform(self, record):
        return record.get_platform_display()

    def render_budget(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_followers(self, value):
        return f"{value:,}"
_ADVERTISEMENT_STATUS_CLASS = {
    "draft": "secondary", "active": "success",
    "paused": "warning", "completed": "info",
}


class AdvertisementTable(tables.Table):
    campaign_name = tables.Column(linkify=True)
    ctr = tables.Column(verbose_name="CTR %", orderable=False, empty_values=())
    budget_used_percent = tables.Column(verbose_name="Budget Used %", orderable=False, empty_values=())
    actions = tables.TemplateColumn(
        template_name="crud/_advertisement_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Advertisement
        fields = ("campaign_name", "product", "platform", "status", "budget", "spent", "clicks", "impressions", "start_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-start_date"

    def render_status(self, record):
        cls = _ADVERTISEMENT_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_platform(self, record):
        return record.get_platform_display()

    def render_budget(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_spent(self, value):
        return format_html("${}", f"{value:,.2f}")

    def render_ctr(self, record):
        return format_html("{}%", record.ctr)

    def render_budget_used_percent(self, record):
        return format_html("{}%", record.budget_used_percent)
_PROMOTION_STATUS_CLASS = {"upcoming": "warning", "live": "success", "expired": "secondary"}
_PARTICIPATION_CLASS = {"open": "primary", "participating": "success", "closed": "secondary"}


class PromotionTable(tables.Table):
    event_name = tables.Column(linkify=True)
    actions = tables.TemplateColumn(
        template_name="crud/_promotion_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Promotion
        fields = ("event_name", "promotion_type", "status", "participation_status", "start_date", "end_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "start_date"

    def render_status(self, record):
        cls = _PROMOTION_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_participation_status(self, record):
        cls = _PARTICIPATION_CLASS.get(record.participation_status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_participation_status_display())

    def render_promotion_type(self, record):
        return record.get_promotion_type_display()
# ============================================================
# ADD THESE IMPORTS TO THE TOP OF crud/tables.py:
# from django.utils.html import format_html
# from .models import PanelUser   (add PanelUser to your existing models import)
#
# THEN ADD THIS CLASS TO THE END OF crud/tables.py
# ============================================================


class PanelUserTable(tables.Table):
    full_name = tables.Column(verbose_name="Name")
    username = tables.Column(accessor="user__username", verbose_name="Username", orderable=False)
    email = tables.Column(accessor="user__email", verbose_name="Email", orderable=False)
    role = tables.Column()
    status = tables.Column()
    actions = tables.TemplateColumn(
        template_name="crud/_paneluser_actions.html",
        orderable=False,
        verbose_name="",
    )

    class Meta:
        model = PanelUser
        fields = ("full_name", "username", "email", "role", "status", "actions")
        attrs = {"class": "table table-hover align-middle"}

    def render_role(self, record):
        return format_html('<span class="badge bg-{}">{}</span>', record.role_color, record.get_role_display())

    def render_status(self, record):
        return format_html('<span class="badge bg-{}">{}</span>', record.status_color, record.get_status_display())