from django import forms

import django_filters as filters
from .models import Advertisement, CatalogUpload, Claim, Company, Contact, ImageBulkUpload, InfluencerCampaign, Inventory, Order, Payment, Pricing, Product, Project, Quality, Return ,Warehouse
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
    product = filters.ModelChoiceFilter(
        queryset=Product.objects.all(), empty_label="All products",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Pricing.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Pricing
        fields = ["product", "status"]



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
    product = filters.ModelChoiceFilter(
        queryset=Product.objects.all(), empty_label="All products",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Inventory.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Inventory
        fields = ["product", "status"]
class CatalogUploadFilter(filters.FilterSet):
    file_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search By File Id"}),
    )
    category = filters.ChoiceFilter(
        choices=CatalogUpload.CATEGORY_CHOICES, empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=CatalogUpload.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = CatalogUpload
        fields = ["file_name", "category", "status"]
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
    product = filters.ModelChoiceFilter(
        queryset=Product.objects.all(), empty_label="All products",
        widget=forms.Select(attrs={"class": "form-select"}),
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
        fields = ["product", "batch_number", "status"]

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search product…"}),
    )
    category = filters.ChoiceFilter(
        choices=Product.CATEGORY_CHOICES, empty_label="All categories",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Product.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Product
        fields = ["name", "category", "status"]

class PaymentFilter(filters.FilterSet):
    order__order_number = filters.CharFilter(
        lookup_expr="icontains",
        label="Order #",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search order #…"}),
    )
    method = filters.ChoiceFilter(
        choices=Payment.METHOD_CHOICES, empty_label="All methods",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Payment.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Payment
        fields = ["order__order_number", "method", "status"]
class WarehouseFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search warehouse…"}),
    )
    location = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search location…"}),
    )
    status = filters.ChoiceFilter(
        choices=Warehouse.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Warehouse
        fields = ["name", "location", "status"]   
class InfluencerCampaignFilter(filters.FilterSet):
    influencer_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search influencer…"}),
    )
    platform = filters.ChoiceFilter(
        choices=InfluencerCampaign.PLATFORM_CHOICES, empty_label="All platforms",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=InfluencerCampaign.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = InfluencerCampaign
        fields = ["influencer_name", "platform", "status"]
class AdvertisementFilter(filters.FilterSet):
    campaign_name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search campaign…"}),
    )
    product = filters.ModelChoiceFilter(
        queryset=Product.objects.all(), empty_label="All products",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    platform = filters.ChoiceFilter(
        choices=Advertisement.PLATFORM_CHOICES, empty_label="All platforms",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Advertisement.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Advertisement
        fields = ["campaign_name", "product", "platform", "status"]