from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse

from .models import CatalogUpload, Claim, Contact, ImageBulkUpload, Inventory, Order, Quality, Return, Pricing
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "customer_email", "product_name", "quantity", "amount", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("customer_name", css_class="col-md-6"),
                Column("customer_email", css_class="col-md-6"),
            ),
            Row(
                Column("product_name", css_class="col-md-6"),
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
        # crispy-forms renders the whole form (Bootstrap 5 markup + csrf) from
        # this helper, so the template is a one-liner: {% crispy form %}.
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
        fields = ["product_name", "sku", "cost_price", "selling_price", "discount_percent", "status", "effective_date"]
        widgets = {
            "effective_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product_name", css_class="col-md-6"),
                Column("sku", css_class="col-md-6"),
            ),
            Row(
                Column("cost_price", css_class="col-md-4"),
                Column("selling_price", css_class="col-md-4"),
                Column("discount_percent", css_class="col-md-4"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
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
        fields = ["product_name", "sku", "quantity", "reorder_level", "warehouse_location", "status", "last_restocked"]
        widgets = {
            "last_restocked": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product_name", css_class="col-md-6"),
                Column("sku", css_class="col-md-6"),
            ),
            Row(
                Column("quantity", css_class="col-md-4"),
                Column("reorder_level", css_class="col-md-4"),
                Column("warehouse_location", css_class="col-md-4"),
            ),
            Row(
                Column("status", css_class="col-md-6"),
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
        fields = ["file_name", "file", "status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("file_name", css_class="col-md-6"),
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
        fields = ["product_name", "batch_number", "inspector_name", "status", "defect_count", "inspection_date", "remarks"]
        widgets = {
            "inspection_date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("product_name", css_class="col-md-6"),
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