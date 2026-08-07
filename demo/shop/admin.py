from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, SiteVisit


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_amount", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(SiteVisit)