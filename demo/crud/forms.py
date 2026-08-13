from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse

from .models import Advertisement,CatalogUpload, CallbackRequest,Claim, Contact, ImageBulkUpload, Inventory,InfluencerCampaign, Order, Quality, Return, Pricing, Product ,Promotion,Payment,Warehouse


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "customer_email", "product", "quantity", "amount", "status"]

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
        }

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
        }

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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product", css_class="col-md-6"),
                Column("warehouse_location", css_class="col-md-6"),
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
        }

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
        }

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
        }

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
        }

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
        }

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
        }

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
class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ["email", "account_name", "mobile_number", "panel_url"]

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
        }

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