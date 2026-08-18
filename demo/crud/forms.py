import re
from django.contrib.auth.models import User
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse
from django.utils import timezone
from django.forms import inlineformset_factory

from shop.models import SupplierProfile
from .models import (
    Advertisement, CatalogUpload, CallbackRequest, Claim, Contact,
    ImageBulkUpload, Inventory, InfluencerCampaign, Order, Quality,
    Return, Pricing, Product, ProductImage, ProductVariant, Promotion,
    Payment, Warehouse, PanelUser
)
NAME_RE = re.compile(r"^[A-Za-z\s]+$")
ALPHANUM_RE = re.compile(r"^[A-Za-z0-9\s\-_&.]+$")
PHONE_RE = re.compile(r"^\+?[0-9\-\s]{7,15}$")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "customer_email", "product", "quantity", "amount", "status"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": 1, "step": 1}),
            "amount": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
        }

    def clean_customer_name(self):
        name = self.cleaned_data.get("customer_name", "").strip()
        if not name:
            raise forms.ValidationError("Customer name is required.")
        if not NAME_RE.match(name):
            raise forms.ValidationError("Customer name can only contain letters and spaces.")
        return name

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("customer_name", css_class="col-md-6"),
                Column("customer_email", css_class="col-md-6"),
            ),
            Row(
                Column("product", css_class="col-md-6"),
                Column("quantity", css_class="col-md-3"),
                Column("amount", css_class="col-md-3"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:order_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "role", "status"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        if not NAME_RE.match(name):
            raise forms.ValidationError("Name can only contain letters and spaces.")
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("email", css_class="col-md-6"),
            ),
            Row(
                Column("role", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:contact_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ["order", "reason", "status", "comments"]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_order(self):
        order = self.cleaned_data.get("order")
        if not order:
            raise forms.ValidationError("Please select an order.")
        return order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("order", css_class="col-md-6"),
                Column("reason", css_class="col-md-6"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
            ),
            "comments",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:return_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ["product", "cost_price", "selling_price", "discount_percent", "status", "effective_date"]
        widgets = {
            "effective_date": forms.DateInput(attrs={"type": "date"}),
            "cost_price": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
            "selling_price": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
            "discount_percent": forms.NumberInput(attrs={"min": 0, "max": 100, "step": 0.01}),
        }

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def clean_cost_price(self):
        cost_price = self.cleaned_data.get("cost_price")
        if cost_price is None or cost_price <= 0:
            raise forms.ValidationError("Cost price must be greater than 0.")
        return cost_price

    def clean_selling_price(self):
        selling_price = self.cleaned_data.get("selling_price")
        if selling_price is None or selling_price <= 0:
            raise forms.ValidationError("Selling price must be greater than 0.")
        return selling_price

    def clean_discount_percent(self):
        discount = self.cleaned_data.get("discount_percent")
        if discount is None or discount < 0 or discount > 100:
            raise forms.ValidationError("Discount percent must be between 0 and 100.")
        return discount

    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get("cost_price")
        selling_price = cleaned_data.get("selling_price")
        if cost_price and selling_price and selling_price < cost_price:
            self.add_error("selling_price", "Selling price should not be lower than cost price.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            Row(
                Column("cost_price", css_class="col-md-4"),
                Column("selling_price", css_class="col-md-4"),
                Column("discount_percent", css_class="col-md-4"),
            ),
            Row(
                Column("effective_date", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:pricing_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ["order", "claim_type", "status", "claim_amount", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "claim_amount": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
        }

    def clean_order(self):
        order = self.cleaned_data.get("order")
        if not order:
            raise forms.ValidationError("Please select an order.")
        return order

    def clean_claim_amount(self):
        amount = self.cleaned_data.get("claim_amount")
        if amount is None or amount <= 0:
            raise forms.ValidationError("Claim amount must be greater than 0.")
        return amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("order", css_class="col-md-6"),
                Column("claim_type", css_class="col-md-6"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
                Column("claim_amount", css_class="col-md-6"),
            ),
            "description",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:claim_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["product", "quantity", "reorder_level", "warehouse", "status", "last_restocked"]
        widgets = {
            "last_restocked": forms.DateInput(attrs={"type": "date"}),
            "quantity": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "reorder_level": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get("reorder_level")
        if reorder_level is None or reorder_level < 0:
            raise forms.ValidationError("Reorder level cannot be negative.")
        return reorder_level

    def clean_last_restocked(self):
        last_restocked = self.cleaned_data.get("last_restocked")
        if last_restocked and last_restocked > timezone.now().date():
            raise forms.ValidationError("Last restocked date cannot be in the future.")
        return last_restocked

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product", css_class="col-md-6"),
                Column("warehouse", css_class="col-md-6"),
            ),
            Row(
                Column("quantity", css_class="col-md-4"),
                Column("reorder_level", css_class="col-md-4"),
                Column("status", css_class="col-md-4"),
            ),
            Row(
                Column("last_restocked", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:inventory_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class CatalogUploadForm(forms.ModelForm):
    class Meta:
        model = CatalogUpload
        fields = ["file_name", "category", "upload_type", "file", "status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_file_name(self):
        file_name = self.cleaned_data.get("file_name", "").strip()
        if not file_name:
            raise forms.ValidationError("File name is required.")
        return file_name

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and not file.name.lower().endswith((".csv", ".xlsx", ".xls")):
            raise forms.ValidationError("Only CSV or Excel files (.csv, .xlsx, .xls) are allowed.")
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("file_name", css_class="col-md-6"),
                Column("category", css_class="col-md-6"),
            ),
            Row(
                Column("upload_type", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            "file",
            "notes",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:catalogupload_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class ImageBulkUploadForm(forms.ModelForm):
    class Meta:
        model = ImageBulkUpload
        fields = ["name", "zip_file", "status", "total_images"]
        widgets = {
            "total_images": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        return name

    def clean_zip_file(self):
        zip_file = self.cleaned_data.get("zip_file")
        if zip_file and not zip_file.name.lower().endswith(".zip"):
            raise forms.ValidationError("Only .zip files are allowed.")
        return zip_file

    def clean_total_images(self):
        total_images = self.cleaned_data.get("total_images")
        if total_images is not None and total_images < 0:
            raise forms.ValidationError("Total images cannot be negative.")
        return total_images

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            "zip_file",
            "total_images",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:imagebulkupload_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = ["product", "batch_number", "inspector_name", "status", "defect_count", "inspection_date", "remarks"]
        widgets = {
            "inspection_date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
            "defect_count": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def clean_batch_number(self):
        batch_number = self.cleaned_data.get("batch_number", "").strip()
        if not batch_number:
            raise forms.ValidationError("Batch number is required.")
        return batch_number

    def clean_inspector_name(self):
        inspector_name = self.cleaned_data.get("inspector_name", "").strip()
        if not inspector_name:
            raise forms.ValidationError("Inspector name is required.")
        if not NAME_RE.match(inspector_name):
            raise forms.ValidationError("Inspector name can only contain letters and spaces.")
        return inspector_name

    def clean_defect_count(self):
        defect_count = self.cleaned_data.get("defect_count")
        if defect_count is None or defect_count < 0:
            raise forms.ValidationError("Defect count cannot be negative.")
        return defect_count

    def clean_inspection_date(self):
        inspection_date = self.cleaned_data.get("inspection_date")
        if inspection_date and inspection_date > timezone.now().date():
            raise forms.ValidationError("Inspection date cannot be in the future.")
        return inspection_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product", css_class="col-md-6"),
                Column("batch_number", css_class="col-md-6"),
            ),
            Row(
                Column("inspector_name", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            Row(
                Column("defect_count", css_class="col-md-6"),
                Column("inspection_date", css_class="col-md-6"),
            ),
            "remarks",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:quality_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "gst_percent", "image", "status", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
            "gst_percent": forms.NumberInput(attrs={"min": 0, "max": 100, "step": 0.01}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Product name is required.")
        if not ALPHANUM_RE.match(name):
            raise forms.ValidationError("Product name contains invalid characters.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean_gst_percent(self):
        gst = self.cleaned_data.get("gst_percent")
        if gst is None or gst < 0 or gst > 100:
            raise forms.ValidationError("GST percent must be between 0 and 100.")
        return gst

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("category", css_class="col-md-6"),
            ),
            Row(
                Column("price", css_class="col-md-6"),
                Column("gst_percent", css_class="col-md-6"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
            ),
            "image",
            "description",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:product_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["order", "amount", "method", "status", "transaction_id", "payment_date", "notes"]
        widgets = {
            "payment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "amount": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
        }

    def clean_order(self):
        order = self.cleaned_data.get("order")
        if not order:
            raise forms.ValidationError("Please select an order.")
        return order

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount

    def clean_payment_date(self):
        payment_date = self.cleaned_data.get("payment_date")
        if payment_date and payment_date > timezone.now():
            raise forms.ValidationError("Payment date cannot be in the future.")
        return payment_date

    def clean_transaction_id(self):
        txn_id = self.cleaned_data.get("transaction_id", "").strip()
        if txn_id and not re.match(r"^[A-Za-z0-9\-_]+$", txn_id):
            raise forms.ValidationError("Transaction ID can only contain letters, numbers, hyphens and underscores.")
        return txn_id

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        order = cleaned_data.get("order")
        if amount and order and amount > order.amount:
            raise forms.ValidationError(f"Payment amount cannot exceed the order amount (${order.amount}).")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("order", css_class="col-md-6"),
                Column("amount", css_class="col-md-6"),
            ),
            Row(
                Column("method", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            Row(
                Column("transaction_id", css_class="col-md-6"),
                Column("payment_date", css_class="col-md-6"),
            ),
            "notes",
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:payment_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location", "address", "capacity", "manager_name", "contact_number", "status"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 2}),
            "capacity": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Warehouse name is required.")
        return name

    def clean_location(self):
        location = self.cleaned_data.get("location", "").strip()
        if not location:
            raise forms.ValidationError("Location is required.")
        return location

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        if capacity is not None and capacity < 0:
            raise forms.ValidationError("Capacity cannot be negative.")
        return capacity

    def clean_manager_name(self):
        manager_name = self.cleaned_data.get("manager_name", "").strip()
        if manager_name and not NAME_RE.match(manager_name):
            raise forms.ValidationError("Manager name can only contain letters and spaces.")
        return manager_name

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number", "").strip()
        if contact_number and not PHONE_RE.match(contact_number):
            raise forms.ValidationError("Enter a valid contact number.")
        return contact_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("location", css_class="col-md-6"),
            ),
            "address",
            Row(
                Column("capacity", css_class="col-md-4"),
                Column("manager_name", css_class="col-md-4"),
                Column("contact_number", css_class="col-md-4"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:warehouse_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class InfluencerCampaignForm(forms.ModelForm):
    class Meta:
        model = InfluencerCampaign
        fields = ["product", "influencer_name", "platform", "followers", "contact",
                  "campaign_name", "budget", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "followers": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "budget": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
        }

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def clean_influencer_name(self):
        name = self.cleaned_data.get("influencer_name", "").strip()
        if not name:
            raise forms.ValidationError("Influencer name is required.")
        return name

    def clean_campaign_name(self):
        name = self.cleaned_data.get("campaign_name", "").strip()
        if not name:
            raise forms.ValidationError("Campaign name is required.")
        return name

    def clean_followers(self):
        followers = self.cleaned_data.get("followers")
        if followers is not None and followers < 0:
            raise forms.ValidationError("Followers cannot be negative.")
        return followers

    def clean_budget(self):
        budget = self.cleaned_data.get("budget")
        if budget is None or budget <= 0:
            raise forms.ValidationError("Budget must be greater than 0.")
        return budget

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before start date.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product", css_class="col-md-6"),
                Column("campaign_name", css_class="col-md-6"),
            ),
            Row(
                Column("influencer_name", css_class="col-md-6"),
                Column("platform", css_class="col-md-6"),
            ),
            Row(
                Column("followers", css_class="col-md-6"),
                Column("contact", css_class="col-md-6"),
            ),
            Row(
                Column("budget", css_class="col-md-4"),
                Column("start_date", css_class="col-md-4"),
                Column("end_date", css_class="col-md-4"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:influencercampaign_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["campaign_name", "product", "platform", "status", "budget", "spent", "clicks", "impressions", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "budget": forms.NumberInput(attrs={"min": 0.01, "step": 0.01}),
            "spent": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
            "clicks": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "impressions": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_campaign_name(self):
        name = self.cleaned_data.get("campaign_name", "").strip()
        if not name:
            raise forms.ValidationError("Campaign name is required.")
        return name

    def clean_product(self):
        product = self.cleaned_data.get("product")
        if not product:
            raise forms.ValidationError("Please select a product.")
        return product

    def clean_budget(self):
        budget = self.cleaned_data.get("budget")
        if budget is None or budget <= 0:
            raise forms.ValidationError("Budget must be greater than 0.")
        return budget

    def clean_spent(self):
        spent = self.cleaned_data.get("spent")
        if spent is not None and spent < 0:
            raise forms.ValidationError("Spent cannot be negative.")
        return spent

    def clean_clicks(self):
        clicks = self.cleaned_data.get("clicks")
        if clicks is not None and clicks < 0:
            raise forms.ValidationError("Clicks cannot be negative.")
        return clicks

    def clean_impressions(self):
        impressions = self.cleaned_data.get("impressions")
        if impressions is not None and impressions < 0:
            raise forms.ValidationError("Impressions cannot be negative.")
        return impressions

    def clean(self):
        cleaned_data = super().clean()
        budget = cleaned_data.get("budget")
        spent = cleaned_data.get("spent")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if budget and spent and spent > budget:
            self.add_error("spent", "Spent cannot exceed the budget.")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before start date.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="crud-card mb-3"><h6 class="fw-bold mb-1">Bid Type</h6><div class="small text-muted mb-3">Ads are billed as Cost Per Click.</div></div>'),
            HTML('<div class="crud-card mb-3"><h6 class="fw-bold mb-3">Catalog Selection</h6>'),
            "campaign_name",
            "product",
            "platform",
            HTML('</div>'),
            HTML('<div class="crud-card mb-3"><h6 class="fw-bold mb-3">Budget</h6>'),
            "budget",
            "spent",
            HTML('</div>'),
            HTML('<div class="crud-card mb-3"><h6 class="fw-bold mb-3">Performance (optional)</h6>'),
            "clicks",
            "impressions",
            HTML('</div>'),
            HTML('<div class="crud-card mb-3"><h6 class="fw-bold mb-3">Duration</h6>'),
            "status",
            "start_date",
            "end_date",
            HTML('</div>'),
            FormActions(
                Submit("save", "Publish Campaign", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:advertisement_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Discard Campaign</a>'
                ),
            ),
        )


class InventoryBulkStockUploadForm(forms.Form):
    file = forms.FileField(
        label="Stock file (CSV)",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv"}),
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and not file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Only .csv files are allowed.")
        return file


class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ["email", "account_name", "mobile_number", "panel_url"]

    def clean_account_name(self):
        account_name = self.cleaned_data.get("account_name", "").strip()
        if not account_name:
            raise forms.ValidationError("Account name is required.")
        return account_name

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number", "").strip()
        if not mobile_number:
            raise forms.ValidationError("Mobile number is required.")
        if not re.match(r"^\+?[0-9]{10,13}$", mobile_number):
            raise forms.ValidationError("Enter a valid mobile number (10-13 digits).")
        return mobile_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "email",
            "account_name",
            "mobile_number",
            "panel_url",
            FormActions(
                Submit("save", "Submit", css_class="btn-primary"),
            ),
        )


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "event_name", "promotion_type", "status", "participation_status",
            "orders_multiplier", "views_multiplier", "expected_customers_crores",
            "start_date", "end_date", "last_day_to_join",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "last_day_to_join": forms.DateInput(attrs={"type": "date"}),
            "orders_multiplier": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
            "views_multiplier": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
            "expected_customers_crores": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
        }

    def clean_event_name(self):
        event_name = self.cleaned_data.get("event_name", "").strip()
        if not event_name:
            raise forms.ValidationError("Event name is required.")
        return event_name

    def clean_orders_multiplier(self):
        value = self.cleaned_data.get("orders_multiplier")
        if value is not None and value < 0:
            raise forms.ValidationError("Orders multiplier cannot be negative.")
        return value

    def clean_views_multiplier(self):
        value = self.cleaned_data.get("views_multiplier")
        if value is not None and value < 0:
            raise forms.ValidationError("Views multiplier cannot be negative.")
        return value

    def clean_expected_customers_crores(self):
        value = self.cleaned_data.get("expected_customers_crores")
        if value is not None and value < 0:
            raise forms.ValidationError("Expected customers cannot be negative.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        last_day_to_join = cleaned_data.get("last_day_to_join")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before start date.")
        if start_date and last_day_to_join and last_day_to_join < start_date:
            self.add_error("last_day_to_join", "Last day to join cannot be before start date.")
        if end_date and last_day_to_join and last_day_to_join > end_date:
            self.add_error("last_day_to_join", "Last day to join cannot be after end date.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("event_name", css_class="col-md-6"),
                Column("promotion_type", css_class="col-md-6"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
                Column("participation_status", css_class="col-md-6"),
            ),
            Row(
                Column("orders_multiplier", css_class="col-md-4"),
                Column("views_multiplier", css_class="col-md-4"),
                Column("expected_customers_crores", css_class="col-md-4"),
            ),
            Row(
                Column("start_date", css_class="col-md-4"),
                Column("end_date", css_class="col-md-4"),
                Column("last_day_to_join", css_class="col-md-4"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:promotion_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )
import re
from django import forms
# from shop.models import SupplierProfile   # <- already imported at top of forms.py


# --- Settings: append these forms to crud/forms.py ---

class WhatsAppSettingsForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ["whatsapp_number", "whatsapp_notifications_enabled"]
        widgets = {
            "whatsapp_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 9876543210",
                "maxlength": "10",
                "pattern": "[6-9][0-9]{9}",
                "inputmode": "numeric",
                "title": "Enter a valid 10-digit Indian mobile number",
            }),
            "whatsapp_notifications_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_whatsapp_number(self):
        number = self.cleaned_data.get("whatsapp_number", "").strip()
        if not number:
            return number
        if not number.isdigit():
            raise forms.ValidationError("Mobile number must contain digits only.")
        if len(number) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        if number[0] not in "6789":
            raise forms.ValidationError("Enter a valid Indian mobile number (must start with 6-9).")
        return number


class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = [
            "bank_account_holder", "bank_account_number",
            "bank_ifsc", "bank_name", "bank_branch",
        ]
        widgets = {
            "bank_account_holder": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Account Holder Name",
                "pattern": "[A-Za-z .]+", "title": "Only letters and spaces allowed",
            }),
            "bank_account_number": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Account Number",
                "maxlength": "18", "inputmode": "numeric",
                "pattern": "[0-9]{9,18}", "title": "9 to 18 digit account number",
            }),
            "bank_ifsc": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "IFSC Code",
                "style": "text-transform:uppercase", "maxlength": "11",
                "pattern": "[A-Za-z]{4}0[A-Za-z0-9]{6}",
                "title": "Format: 4 letters + 0 + 6 alphanumeric (e.g. HDFC0001234)",
            }),
            "bank_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Bank Name"}),
            "bank_branch": forms.TextInput(attrs={"class": "form-control", "placeholder": "Branch"}),
        }

    def clean_bank_account_holder(self):
        name = self.cleaned_data.get("bank_account_holder", "").strip()
        if not name:
            raise forms.ValidationError("Account holder name is required.")
        if not re.match(r"^[A-Za-z .]+$", name):
            raise forms.ValidationError("Only letters and spaces are allowed.")
        return name

    def clean_bank_account_number(self):
        number = self.cleaned_data.get("bank_account_number", "").strip()
        if not number:
            raise forms.ValidationError("Account number is required.")
        if not number.isdigit():
            raise forms.ValidationError("Account number must contain digits only.")
        if not (9 <= len(number) <= 18):
            raise forms.ValidationError("Account number must be 9 to 18 digits long.")
        return number

    def clean_bank_ifsc(self):
        ifsc = self.cleaned_data.get("bank_ifsc", "").upper().strip()
        if not ifsc:
            raise forms.ValidationError("IFSC code is required.")
        if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", ifsc):
            raise forms.ValidationError("Invalid IFSC format (e.g. HDFC0001234).")
        return ifsc

    def clean_bank_name(self):
        name = self.cleaned_data.get("bank_name", "").strip()
        if not name:
            raise forms.ValidationError("Bank name is required.")
        return name

    def clean_bank_branch(self):
        branch = self.cleaned_data.get("bank_branch", "").strip()
        if not branch:
            raise forms.ValidationError("Branch is required.")
        return branch


class TaxDetailsForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ["gstin", "pan_number"]
        widgets = {
            "gstin": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "22AAAAA0000A1Z5",
                "style": "text-transform:uppercase", "maxlength": "15",
                "pattern": "[0-9]{2}[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}[1-9A-Za-z]{1}Z[0-9A-Za-z]{1}",
                "title": "Enter a valid 15-character GSTIN",
            }),
            "pan_number": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "AAAAA0000A",
                "style": "text-transform:uppercase", "maxlength": "10",
                "pattern": "[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}",
                "title": "Enter a valid 10-character PAN",
            }),
        }

    def clean_gstin(self):
        gstin = self.cleaned_data.get("gstin", "").upper().strip()
        if not gstin:
            raise forms.ValidationError("GSTIN is required.")
        if not re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", gstin):
            raise forms.ValidationError("Invalid GSTIN format (e.g. 22AAAAA0000A1Z5).")
        return gstin

    def clean_pan_number(self):
        pan = self.cleaned_data.get("pan_number", "").upper().strip()
        if not pan:
            raise forms.ValidationError("PAN is required.")
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan):
            raise forms.ValidationError("Invalid PAN format (e.g. AAAAA0000A).")
        return pan


class SupplierSignatureForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ["signature_text", "signature_image"]
        widgets = {
            "signature_text": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Type your signature",
                "maxlength": "150",
            }),
            "signature_image": forms.ClearableFileInput(attrs={
                "class": "form-control", "accept": "image/png,image/jpeg,image/jpg",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("signature_text", "")
        image = cleaned_data.get("signature_image")
        if not text and not image:
            raise forms.ValidationError(
                "Provide either a text signature or upload a signature image."
            )
        return cleaned_data

    def clean_signature_image(self):
        image = self.cleaned_data.get("signature_image")
        if image and hasattr(image, "content_type"):
            if image.content_type not in ("image/png", "image/jpeg"):
                raise forms.ValidationError("Only PNG or JPEG images are allowed.")
            max_size_mb = 2
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(f"Image size must be under {max_size_mb}MB.")
        return image


class EmailNotificationsForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ["notification_email", "email_notifications_enabled"]
        widgets = {
            "notification_email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "you@example.com",
            }),
            "email_notifications_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_notification_email(self):
        email = self.cleaned_data.get("notification_email", "").strip()
        enabled = self.data.get("email_notifications_enabled")
        if enabled and not email:
            raise forms.ValidationError(
                "Provide an email address to enable email notifications."
            )
        return email
# ============================================================
# ADD THIS IMPORT TO THE TOP OF crud/forms.py:
# from django.contrib.auth.models import User
# from .models import PanelUser   (add PanelUser to your existing models import)
#
# THEN ADD THIS CLASS TO THE END OF crud/forms.py
# ============================================================


# ============================================================
# REPLACE your existing PanelUserForm's __init__ method with this version
# (adds a crispy FormHelper so the modal shows a Submit button).
#
# ADD THIS IMPORT TO THE TOP OF crud/forms.py (if not already present):
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# ============================================================


class PanelUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Login username"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@example.com"}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Set login password",
        }),
        help_text="New user માટે required. Edit કરતી વખતે ખાલી રાખો તો current password રહેશે.",
    )

    class Meta:
        model = PanelUser
        fields = ["full_name", "role", "phone", "status"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Editing an existing panel user: prefill + lock username
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email
            self.fields["username"].widget.attrs["readonly"] = True
            self.fields["password"].help_text = "ખાલી રાખો તો current password બદલાશે નહીં."

        # --- crispy form: adds the Submit button in the modal ---
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = "post"
        submit_label = "Update" if self.instance and self.instance.pk else "Create User"
        self.helper.add_input(Submit("submit", submit_label, css_class="btn btn-primary w-100 mt-2"))

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = User.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user_id)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user_id)
        if qs.exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        is_new = not (self.instance and self.instance.pk)
        if is_new and not password:
            raise forms.ValidationError("Password is required for new users.")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        panel_user = super().save(commit=False)
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data.get("password")

        if panel_user.pk and panel_user.user_id:
            user = panel_user.user
        else:
            user = User(username=username)

        user.username = username
        user.email = email
        user.is_staff = True
        if password:
            user.set_password(password)

        if commit:
            user.save()
            panel_user.user = user
            panel_user.save()
        return panel_user
# --- Inline formsets for Product gallery images & size variants ---

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=["image", "order"],
    extra=1, can_delete=True,
    widgets={
        "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        "order": forms.NumberInput(attrs={"class": "form-control", "min": 0, "style": "width:80px"}),
    },
)

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant,
    fields=["size", "stock", "price_adjustment"],
    extra=1, can_delete=True,
    widgets={
        "size": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Free Size, M, L"}),
        "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        "price_adjustment": forms.NumberInput(attrs={"class": "form-control", "step": 0.01, "min": 0}),
    },
)