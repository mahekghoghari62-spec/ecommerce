from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
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