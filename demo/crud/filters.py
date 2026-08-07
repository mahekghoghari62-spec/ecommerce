from django import forms

import django_filters as filters
from .models import CatalogUpload, Claim, Company, Contact, ImageBulkUpload, Inventory, Order, Pricing, Project, Quality, Return
class OrderFilter(filters.FilterSet):
    order_number = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search order #…"}),
    )
    customer_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search customer…"}),
    )
    status = filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Order
        fields = ["order_number", "customer_name", "status"]


class ContactFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search name…"}),
    )
    role = filters.ChoiceFilter(
        choices=Contact.ROLE_CHOICES, empty_label="All roles",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Contact.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Contact
        fields = ["name", "role", "status"]


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search project…"}),
    )
    company = filters.ModelChoiceFilter(
        queryset=Company.objects.all(), empty_label="All companies",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Project.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Project
        fields = ["name", "company", "status"]


class ReturnFilter(filters.FilterSet):
    order__order_number = filters.CharFilter(
        lookup_expr="icontains",
        label="Order #",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search order #…"}),
    )
    reason = filters.ChoiceFilter(
        choices=Return.REASON_CHOICES, empty_label="All reasons",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Return.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Return
        fields = ["order__order_number", "reason", "status"]


class PricingFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search product…"}),
    )
    sku = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search SKU…"}),
    )
    status = filters.ChoiceFilter(
        choices=Pricing.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Pricing
        fields = ["product_name", "sku", "status"]


class ClaimFilter(filters.FilterSet):
    order__order_number = filters.CharFilter(
        lookup_expr="icontains",
        label="Order #",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search order #…"}),
    )
    claim_type = filters.ChoiceFilter(
        choices=Claim.TYPE_CHOICES, empty_label="All types",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Claim.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Claim
        fields = ["order__order_number", "claim_type", "status"]


class InventoryFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search product…"}),
    )
    sku = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search SKU…"}),
    )
    status = filters.ChoiceFilter(
        choices=Inventory.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Inventory
        fields = ["product_name", "sku", "status"]
class CatalogUploadFilter(filters.FilterSet):
    file_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search file name…"}),
    )
    status = filters.ChoiceFilter(
        choices=CatalogUpload.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = CatalogUpload
        fields = ["file_name", "status"]
class ImageBulkUploadFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search name…"}),
    )
    status = filters.ChoiceFilter(
        choices=ImageBulkUpload.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = ImageBulkUpload
        fields = ["name", "status"]
class QualityFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search product…"}),
    )
    batch_number = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search batch…"}),
    )
    status = filters.ChoiceFilter(
        choices=Quality.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Quality
        fields = ["product_name", "batch_number", "status"]