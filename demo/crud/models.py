from django.db import models
from django.urls import reverse
from django.utils import timezone

class Company(models.Model):
    INDUSTRY_CHOICES = [
        ("tech", "Technology"), ("finance", "Finance"), ("health", "Healthcare"),
        ("retail", "Retail"), ("media", "Media"),
    ]
    name = models.CharField(max_length=120, unique=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, default="tech")
    website = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField(blank=True)
    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    order_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        return self.order_number

    def get_absolute_url(self):
        return reverse("crud:order_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "pending": "warning", "processing": "info", "shipped": "primary",
            "delivered": "success", "cancelled": "danger",
        }.get(self.status, "secondary")

    def save(self, *args, **kwargs):
        if not self.order_number:
            last = Order.objects.order_by("-id").first()
            next_id = (last.id + 1) if last else 1
            self.order_number = f"ORD-{next_id:05d}"
        super().save(*args, **kwargs)


class Contact(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("editor", "Editor"), ("viewer", "Viewer")]
    STATUS_CHOICES = [("active", "Active"), ("pending", "Pending"), ("disabled", "Disabled")]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:contact_update", args=[self.pk])


class Tag(models.Model):
    COLOR_CHOICES = [
        ("primary", "Primary"), ("success", "Success"), ("info", "Info"),
        ("warning", "Warning"), ("danger", "Danger"), ("secondary", "Secondary"),
    ]
    name = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="secondary")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"), ("active", "Active"),
        ("on_hold", "On hold"), ("completed", "Completed"),
    ]
    name = models.CharField(max_length=140)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    lead = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="led_projects"
    )
    team = models.ManyToManyField(Contact, blank=True, related_name="projects")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:project_detail", args=[self.pk])

    @property
    def status_color(self):
        return {"planning": "info", "active": "success", "on_hold": "warning",
                "completed": "secondary"}.get(self.status, "secondary")


class Task(models.Model):
    STATUS_CHOICES = [("todo", "To do"), ("in_progress", "In progress"), ("done", "Done")]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    assignee = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks"
    )
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def status_color(self):
        return {"todo": "secondary", "in_progress": "info", "done": "success"}.get(self.status, "secondary")

class Return(models.Model):
    REASON_CHOICES = [
        ("defective", "Defective Product"),
        ("wrong_item", "Wrong Item Sent"),
        ("not_needed", "No Longer Needed"),
        ("size_issue", "Size/Fit Issue"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("picked_up", "Picked Up"),
        ("refunded", "Refunded"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="returns")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="requested")
    comments = models.TextField(blank=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-requested_date"]

    def __str__(self):
        return f"Return for {self.order.order_number}"

    def get_absolute_url(self):
        return reverse("crud:return_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "requested": "warning", "approved": "info", "rejected": "danger",
            "picked_up": "primary", "refunded": "success",
        }.get(self.status, "secondary")
class Pricing(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("draft", "Draft"),
        ("archived", "Archived"),
    ]

    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="pricings")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    effective_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-effective_date"]
        verbose_name_plural = "pricing"

    def __str__(self):
        return f"{self.product} ({self.sku})" if self.sku else self.product.name

    def get_absolute_url(self):
        return reverse("crud:pricing_update", args=[self.pk])

    @property
    def status_color(self):
        return {"active": "success", "draft": "warning", "archived": "secondary"}.get(self.status, "secondary")

    @property
    def final_price(self):
        discount_amount = (self.selling_price * self.discount_percent) / 100
        return self.selling_price - discount_amount

    @property
    def margin_percent(self):
        if self.cost_price and self.cost_price > 0:
            return round(((self.selling_price - self.cost_price) / self.cost_price) * 100, 2)
        return 0
class Claim(models.Model):
    TYPE_CHOICES = [
        ("damaged", "Damaged Product"),
        ("lost", "Lost in Transit"),
        ("missing_item", "Missing Item"),
        ("quality_issue", "Quality Issue"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("under_review", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("settled", "Settled"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="claims")
    claim_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    filed_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-filed_date"]

    def __str__(self):
        return f"Claim for {self.order.order_number}"

    def get_absolute_url(self):
        return reverse("crud:claim_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "open": "warning", "under_review": "info", "approved": "primary",
            "rejected": "danger", "settled": "success",
        }.get(self.status, "secondary")
class Inventory(models.Model):
    STATUS_CHOICES = [
        ("in_stock", "In Stock"),
        ("low_stock", "Low Stock"),
        ("out_of_stock", "Out of Stock"),
        ("discontinued", "Discontinued"),
    ]

    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="inventory_items")

    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    warehouse = models.ForeignKey(
        "Warehouse", on_delete=models.SET_NULL, null=True, blank=True, related_name="inventory_items"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_stock")
    last_restocked = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product"]
        verbose_name_plural = "inventory"

    def __str__(self):
        return str(self.product)

    def get_absolute_url(self):
        return reverse("crud:inventory_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "in_stock": "success", "low_stock": "warning",
            "out_of_stock": "danger", "discontinued": "secondary",
        }.get(self.status, "secondary")

    @property
    def is_low(self):
        return self.quantity <= self.reorder_level

    def save(self, *args, **kwargs):
        # Auto-update status based on quantity (only if not manually discontinued)
        if self.status != "discontinued":
            if self.quantity == 0:
                self.status = "out_of_stock"
            elif self.quantity <= self.reorder_level:
                self.status = "low_stock"
            else:
                self.status = "in_stock"
        super().save(*args, **kwargs)
class CatalogUpload(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    CATEGORY_CHOICES = [
        ("gowns_ethnic", "Gowns - Ethnic"),
        ("top_bottom_sets", "Top & Bottom Sets"),
        ("kurti_dupatta", "Kurti With Dupatta"),
        ("kurtis", "Kurtis"),
        ("sarees", "Sarees"),
        ("other", "Other"),
    ]
    UPLOAD_TYPE_CHOICES = [
        ("bulk", "Bulk Upload"),
        ("single", "Single Upload"),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="other")
    upload_type = models.CharField(max_length=10, choices=UPLOAD_TYPE_CHOICES, default="bulk")
    file_name = models.CharField(max_length=200)
    file = models.FileField(upload_to="catalog_uploads/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_rows = models.PositiveIntegerField(default=0)
    processed_rows = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_date"]

    def __str__(self):
        return self.file_name

    def get_absolute_url(self):
        return reverse("crud:catalogupload_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "pending": "warning", "processing": "info",
            "completed": "success", "failed": "danger",
        }.get(self.status, "secondary")

    @property
    def success_rate(self):
        if self.total_rows > 0:
            return round((self.processed_rows / self.total_rows) * 100, 1)
        return 0
class ImageBulkUpload(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=200)
    zip_file = models.FileField(upload_to="image_bulk_uploads/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_images = models.PositiveIntegerField(default=0)
    processed_images = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_date"]

    def __str__(self):
        return self.name

    @property
    def success_rate(self):
        if self.total_images == 0:
            return 0
        return round((self.processed_images - self.error_count) * 100 / self.total_images)

    def get_absolute_url(self):
        return reverse("crud:imagebulkupload_update", args=[self.pk])
class Quality(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("rework", "Rework"),
    ]

    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="quality_checks")
    batch_number = models.CharField(max_length=50)
    inspector_name = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    defect_count = models.PositiveIntegerField(default=0)
    inspection_date = models.DateField()
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-inspection_date"]
        verbose_name_plural = "Quality checks"

    def __str__(self):
        return f"{self.product.name} — {self.batch_number}"

    def get_absolute_url(self):
        return reverse("crud:quality_update", args=[self.pk])
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("electronics", "Electronics"),
        ("fashion", "Fashion"),
        ("home", "Home & Kitchen"),
        ("beauty", "Beauty"),
        ("grocery", "Grocery"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("draft", "Draft"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="GST % e.g. 18.00")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:product_update", args=[self.pk])

    @property
    def status_color(self):
        return {"active": "success", "draft": "warning", "inactive": "secondary"}.get(self.status, "secondary")

    @property
    def selling_price(self):
        gst_amount = (self.price * self.gst_percent) / 100
        return self.price + gst_amount


class Payment(models.Model):
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
        ("bank_transfer", "Bank Transfer"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="cash")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment for {self.order.order_number}"

    def get_absolute_url(self):
        return reverse("crud:payment_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "pending": "warning", "completed": "success",
            "failed": "danger", "refunded": "secondary",
        }.get(self.status, "secondary")
class Warehouse(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("under_maintenance", "Under Maintenance"),
    ]

    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text="Max storage units")
    manager_name = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:warehouse_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "active": "success", "inactive": "secondary", "under_maintenance": "warning",
        }.get(self.status, "secondary")
class InfluencerCampaign(models.Model):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("facebook", "Facebook"),
        ("twitter", "Twitter/X"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="influencer_campaigns")
    influencer_name = models.CharField(max_length=150)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="instagram")
    followers = models.PositiveIntegerField(default=0)
    contact = models.CharField(max_length=100, blank=True)
    campaign_name = models.CharField(max_length=150)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Influencer campaign"
        verbose_name_plural = "Influencer campaigns"

    def __str__(self):
        return f"{self.campaign_name} — {self.influencer_name}"

    def get_absolute_url(self):
        return reverse("crud:influencercampaign_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "planned": "info", "active": "success",
            "completed": "secondary", "cancelled": "danger",
        }.get(self.status, "secondary")
class Advertisement(models.Model):
    PLATFORM_CHOICES = [
        ("app_banner", "App Banner"),
        ("search_ads", "Search Ads"),
        ("social_media", "Social Media"),
        ("email", "Email Campaign"),
        ("push_notification", "Push Notification"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    ]

    campaign_name = models.CharField(max_length=150)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="advertisements")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="app_banner")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.campaign_name

    def get_absolute_url(self):
        return reverse("crud:advertisement_update", args=[self.pk])

    @property
    def status_color(self):
        return {
            "draft": "secondary", "active": "success",
            "paused": "warning", "completed": "info",
        }.get(self.status, "secondary")

    @property
    def ctr(self):
        """Click-through rate %"""
        if self.impressions > 0:
            return round((self.clicks / self.impressions) * 100, 2)
        return 0

    @property
    def budget_used_percent(self):
        if self.budget > 0:
            return round((self.spent / self.budget) * 100, 1)
        return 0
class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ("needs_attention", "Needs Attention"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    issue = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="needs_attention")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.ticket_id} — {self.issue}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            last = SupportTicket.objects.order_by("-id").first()
            next_id = (last.id + 1) if last else 1
            self.ticket_id = f"{8768000000000 + next_id}"
        super().save(*args, **kwargs)

    @property
    def status_color(self):
        return {
            "needs_attention": "danger", "in_progress": "warning", "closed": "success",
        }.get(self.status, "secondary")
class PayoutCycle(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
    ]

    cycle_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    sales_returns = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ads_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    program_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    program_benefits = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    referral_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neft_id = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["cycle_date"]

    def __str__(self):
        return f"Payout {self.cycle_date} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse("crud:payoutcycle_update", args=[self.pk])

    @property
    def net_amount(self):
        return (
            self.sales_returns
            - self.ads_cost
            - self.program_cost
            + self.program_benefits
            + self.referral_earnings
        )


class CompensationRecovery(models.Model):
    TYPE_CHOICES = [
        ("compensation", "Compensation"),
        ("recovery", "Recovery"),
    ]

    record_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="compensation")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_record_type_display()} — {self.amount}"

    def get_absolute_url(self):
        return reverse("crud:compensationrecovery_update", args=[self.pk])
class CallbackRequest(models.Model):
    email = models.EmailField()
    account_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=20)
    panel_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Callback — {self.account_name}"
class Promotion(models.Model):
    TYPE_CHOICES = [
        ("sale_event", "Sale Event"),
        ("flexi_growth", "Flexi Growth Offer"),
        ("deal", "Deal"),
        ("flash_event", "Flash Event"),
    ]
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("expired", "Expired"),
    ]
    PARTICIPATION_CHOICES = [
        ("open", "Open for Participation"),
        ("participating", "Participating"),
        ("closed", "Closed"),
    ]

    event_name = models.CharField(max_length=150)
    promotion_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="sale_event")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    participation_status = models.CharField(max_length=20, choices=PARTICIPATION_CHOICES, default="open")
    orders_multiplier = models.PositiveIntegerField(default=1, help_text="e.g. 10 for 'Upto 10 times more orders'")
    views_multiplier = models.PositiveIntegerField(default=1, help_text="e.g. 10 for 'Upto 10 times more views'")
    expected_customers_crores = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_day_to_join = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse("crud:promotion_update", args=[self.pk])

    @property
    def status_color(self):
        return {"upcoming": "warning", "live": "success", "expired": "secondary"}.get(self.status, "secondary")

    @property
    def participation_color(self):
        return {"open": "primary", "participating": "success", "closed": "secondary"}.get(self.participation_status, "secondary")
class DailyMetric(models.Model):
    date = models.DateField(unique=True)
    total_views = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"Metrics {self.date}"