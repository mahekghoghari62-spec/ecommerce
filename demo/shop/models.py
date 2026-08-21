from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.CASCADE, related_name="children"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.parent} > {self.name}" if self.parent_id else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_descendant_ids(self):
        """This category's id + all nested children ids (used for category-mode filtering)."""
        ids = [self.id]
        for child in self.children.all():
            ids += child.get_descendant_ids()
        return ids


class Product(models.Model):
    supplier = models.ForeignKey(
        "SupplierProfile", on_delete=models.CASCADE,
        null=True, blank=True, related_name="products"
    )
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class SiteVisit(models.Model):
    """Simple visitor counter — one row per page hit, used for the dashboard chart."""
    visited_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255, blank=True)


class SupplierProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="supplier_profile")

    CATEGORY_MODE_CHOICES = [
        ("single", "Single Category (Clothes only)"),
        ("multiple", "Multiple Category"),
    ]
    category_mode = models.CharField(
        max_length=10, choices=CATEGORY_MODE_CHOICES, default="multiple"
    )

    # WhatsApp Notifications
    whatsapp_number = models.CharField(max_length=15, blank=True)
    whatsapp_notifications_enabled = models.BooleanField(default=True)

    # Bank Details
    bank_account_holder = models.CharField(max_length=150, blank=True)
    bank_account_number = models.CharField(max_length=30, blank=True)
    bank_ifsc = models.CharField(max_length=15, blank=True)
    bank_name = models.CharField(max_length=150, blank=True)
    bank_branch = models.CharField(max_length=150, blank=True)

    # Tax Details
    gstin = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)

    # Supplier Signature
    signature_text = models.CharField(max_length=150, blank=True)
    signature_image = models.ImageField(upload_to="signatures/", blank=True, null=True)

    # Email Notifications
    email_notifications_enabled = models.BooleanField(default=True)
    notification_email = models.EmailField(blank=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile — {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile — {self.user.username}"


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ("home", "Home"),
        ("work", "Work"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default="home")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.city}"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart — {self.user.username}"

    @property
    def active_items(self):
        return self.items.filter(saved_for_later=False)

    @property
    def saved_items(self):
        return self.items.filter(saved_for_later=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.active_items)

    @property
    def subtotal(self):
        return sum(item.product.price * item.quantity for item in self.active_items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("crud.Product", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    saved_for_later = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.product.price * self.quantity
class SiteSettings(models.Model):
    """Single site-wide row controlling whether the public shop nav shows
    only Clothes or all categories, independent of any one supplier."""

    CATEGORY_MODE_CHOICES = [
        ("single", "Single Category (Clothes only)"),
        ("multiple", "Multiple Category"),
    ]
    category_mode = models.CharField(
        max_length=10, choices=CATEGORY_MODE_CHOICES, default="multiple"
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Site Settings ({self.get_category_mode_display()})"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj