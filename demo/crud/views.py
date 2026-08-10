from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView,UpdateView
from django.db import models
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from .mixins import AjaxModalDeleteMixin, AjaxModalFormMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from .filters import AdvertisementFilter, CatalogUploadFilter, ClaimFilter, ContactFilter, ImageBulkUploadFilter, InfluencerCampaignFilter, InventoryFilter, OrderFilter, PaymentFilter, PricingFilter, ProductFilter, ProjectFilter, QualityFilter, ReturnFilter, WarehouseFilter
from .forms import AdvertisementForm, CatalogUploadForm, ClaimForm, ContactForm, ImageBulkUploadForm, InfluencerCampaignForm, InventoryForm, OrderForm, PaymentForm, PricingForm, ProductForm, QualityForm, ReturnForm, WarehouseForm
from .models import Advertisement, CatalogUpload, Claim, Contact, ImageBulkUpload, InfluencerCampaign, Inventory, Order, Payment, Pricing, Product, Project, Quality, Return,SupportTicket, Warehouse
from .tables import AdvertisementTable, CatalogUploadTable, ClaimTable, ContactTable, ImageBulkUploadTable, InfluencerCampaignTable, InventoryTable, OrderTable, PaymentTable, PricingTable, ProductTable, ProjectTable, QualityTable, ReturnTable, WarehouseTable
import csv
import io
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views import View
from .forms import InventoryBulkStockUploadForm

# --- Orders: full CRUD (tables2 + django-filter + crispy form + messages) ---
class OrderListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = "crud/order_list.html"
    table_pagination = {"per_page": 10}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_tabs"] = [
            {"key": key, "label": label, "count": Order.objects.filter(status=key).count()}
            for key, label in Order.STATUS_CHOICES
        ]
        context["total_count"] = Order.objects.count()
        context["active_status"] = self.request.GET.get("status", "")
        return context


class OrderCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "crud/order_form.html"
    success_url = reverse_lazy("crud:order_list")

    def form_valid(self, form):
        messages.success(self.request, f"Order created for “{form.instance.customer_name}”.")
        return super().form_valid(form)


class OrderUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "crud/order_form.html"
    success_url = reverse_lazy("crud:order_list")

    def form_valid(self, form):
        messages.success(self.request, f"Order “{form.instance.order_number}” updated.")
        return super().form_valid(form)


class OrderDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Order
    template_name = "crud/order_confirm_delete.html"
    success_url = reverse_lazy("crud:order_list")

    def form_valid(self, form):
        messages.success(self.request, f"Order “{self.object.order_number}” deleted.")
        return super().form_valid(form)


# --- Contacts: full CRUD (tables2 + django-filter + crispy form + messages) ---
class ContactListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Contact
    table_class = ContactTable
    filterset_class = ContactFilter
    template_name = "crud/contact_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("company")


class ContactCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” created.")
        return super().form_valid(form)


class ContactUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” updated.")
        return super().form_valid(form)


class ContactDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "crud/contact_confirm_delete.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{self.object.name}” deleted.")
        return super().form_valid(form)


# --- Projects: relational list + detail (showcases FK / M2M data) ---
class ProjectListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Project
    table_class = ProjectTable
    filterset_class = ProjectFilter
    template_name = "crud/project_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("company", "lead")
            .prefetch_related("team", "tags")
        )


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "crud/project_detail.html"

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("company", "lead")
            .prefetch_related("team", "tags", "tasks__assignee")
        )


# --- Returns: full CRUD (tables2 + django-filter + crispy form + messages) ---
class ReturnListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Return
    table_class = ReturnTable
    filterset_class = ReturnFilter
    template_name = "crud/return_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_returns = Return.objects.all()
        context["total_returns"] = all_returns.count()
        context["requested_count"] = all_returns.filter(status="requested").count()
        context["approved_count"] = all_returns.filter(status="approved").count()
        context["rejected_count"] = all_returns.filter(status="rejected").count()
        context["picked_up_count"] = all_returns.filter(status="picked_up").count()
        context["refunded_count"] = all_returns.filter(status="refunded").count()

        all_claims = Claim.objects.select_related("order")
        context["claim_table"] = ClaimTable(all_claims)
        context["total_claims"] = all_claims.count()
        context["open_claims_count"] = all_claims.filter(status="open").count()
        context["under_review_claims_count"] = all_claims.filter(status="under_review").count()
        context["approved_claims_count"] = all_claims.filter(status="approved").count()
        context["rejected_claims_count"] = all_claims.filter(status="rejected").count()
        context["settled_claims_count"] = all_claims.filter(status="settled").count()
        return context


class ReturnCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Return
    form_class = ReturnForm
    template_name = "crud/return_form.html"
    success_url = reverse_lazy("crud:return_list")

    def form_valid(self, form):
        messages.success(self.request, f"Return created for order “{form.instance.order.order_number}”.")
        return super().form_valid(form)


class ReturnUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Return
    form_class = ReturnForm
    template_name = "crud/return_form.html"
    success_url = reverse_lazy("crud:return_list")

    def form_valid(self, form):
        messages.success(self.request, f"Return for “{form.instance.order.order_number}” updated.")
        return super().form_valid(form)


class ReturnDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Return
    template_name = "crud/return_confirm_delete.html"
    success_url = reverse_lazy("crud:return_list")

    def form_valid(self, form):
        messages.success(self.request, f"Return for “{self.object.order.order_number}” deleted.")
        return super().form_valid(form)


# --- Pricing: full CRUD (tables2 + django-filter + crispy form + messages) ---
class PricingListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Pricing
    table_class = PricingTable
    filterset_class = PricingFilter
    template_name = "crud/pricing_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pricing = Pricing.objects.select_related("product")
        context["total_pricing"] = all_pricing.count()
        context["active_count"] = all_pricing.filter(status="active").count()
        context["draft_count"] = all_pricing.filter(status="draft").count()
        context["archived_count"] = all_pricing.filter(status="archived").count()

        context["active_table"] = PricingTable(all_pricing.filter(status="active"), prefix="active-")
        context["draft_table"] = PricingTable(all_pricing.filter(status="draft"), prefix="draft-")
        context["archived_table"] = PricingTable(all_pricing.filter(status="archived"), prefix="archived-")

        active_items = all_pricing.filter(status="active")
        if active_items.exists():
            avg_margin = sum(p.margin_percent for p in active_items) / active_items.count()
            context["avg_margin"] = round(avg_margin, 1)
        else:
            context["avg_margin"] = 0

        context["losing_margin_count"] = active_items.filter(
            selling_price__lte=models.F("cost_price")
        ).count()
        return context
class PricingCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Pricing
    form_class = PricingForm
    template_name = "crud/pricing_form.html"
    success_url = reverse_lazy("crud:pricing_list")

    def form_valid(self, form):
        messages.success(self.request, f"Pricing created for “{form.instance.product.name}”.")
        return super().form_valid(form)


class PricingUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Pricing
    form_class = PricingForm
    template_name = "crud/pricing_form.html"
    success_url = reverse_lazy("crud:pricing_list")

    def form_valid(self, form):
        messages.success(self.request, f"Pricing for “{form.instance.product.name}” updated.")
        return super().form_valid(form)


class PricingDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Pricing
    template_name = "crud/pricing_confirm_delete.html"
    success_url = reverse_lazy("crud:pricing_list")

    def form_valid(self, form):
        messages.success(self.request, f"Pricing for “{self.object.product.name}” deleted.")
        return super().form_valid(form)


# --- Claims: full CRUD (tables2 + django-filter + crispy form + messages) ---
class ClaimListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Claim
    table_class = ClaimTable
    filterset_class = ClaimFilter
    template_name = "crud/claim_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_claims = Claim.objects.all()
        context["total_claims"] = all_claims.count()
        context["open_count"] = all_claims.filter(status="open").count()
        context["approved_count"] = all_claims.filter(status="approved").count()
        context["settled_count"] = all_claims.filter(status="settled").count()
        return context

class ClaimCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = "crud/claim_form.html"
    success_url = reverse_lazy("crud:claim_list")

    def form_valid(self, form):
        messages.success(self.request, f"Claim created for order “{form.instance.order.order_number}”.")
        return super().form_valid(form)


class ClaimUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Claim
    form_class = ClaimForm
    template_name = "crud/claim_form.html"
    success_url = reverse_lazy("crud:claim_list")

    def form_valid(self, form):
        messages.success(self.request, f"Claim for “{form.instance.order.order_number}” updated.")
        return super().form_valid(form)


class ClaimDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Claim
    template_name = "crud/claim_confirm_delete.html"
    success_url = reverse_lazy("crud:claim_list")

    def form_valid(self, form):
        messages.success(self.request, f"Claim for “{self.object.order.order_number}” deleted.")
        return super().form_valid(form)
class SupportView(LoginRequiredMixin, TemplateView):
    template_name = "crud/support.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = SupportTicket.objects.all()
        context["tickets"] = tickets
        context["all_count"] = tickets.count()
        context["needs_attention_count"] = tickets.filter(status="needs_attention").count()
        context["in_progress_count"] = tickets.filter(status="in_progress").count()
        context["closed_count"] = tickets.filter(status="closed").count()
        context["active_tab"] = self.request.GET.get("tab", "help")
        return context

class SupportView(LoginRequiredMixin, TemplateView):
    template_name = "crud/support.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = SupportTicket.objects.all()
        context["tickets"] = tickets
        context["all_count"] = tickets.count()
        context["needs_attention_count"] = tickets.filter(status="needs_attention").count()
        context["in_progress_count"] = tickets.filter(status="in_progress").count()
        context["closed_count"] = tickets.filter(status="closed").count()
        context["active_tab"] = self.request.GET.get("tab", "help")

        context["return_help_topics"] = [
            "I have received wrong return", "I have received damaged return",
            "I have not received my Return/RTO shipment", "Item/s are missing in my return",
            "I have received a wrong barcoded package in RTO", "I have received used product as return",
            "Return/RTO product not received but marked delivered - Need Proof of Delivery",
            "I have an issue with Exchange order",
            "Return/RTO Delivery Issue - False Attempt by Logistic Partner",
            "I am not able to generate invoice for exchange order",
            "I have received an RTO in a non-barcoded package",
            "I am unable to raise Wrong Return / RTO claims",
            "Order return shipping charge fee issue",
            "When will I receive my wrong return related compensation",
            "I want to stop using the Wrong/Defective Returns Feature",
            "My order has been marked as Returnless Refund. What is Returnless Refund?",
            "Other Returns/RTO and Exchange related issue",
        ]
        context["help_categories"] = [
            "Cataloging & Pricing", "Orders & Delivery", "Payments", "Inventory",
            "Account", "Advertisements & Promotions", "Instant Cash", "Others",
        ]
        return context
# --- Inventory: full CRUD (tables2 + django-filter + crispy form + messages) ---
class InventoryListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Inventory
    table_class = InventoryTable
    filterset_class = InventoryFilter
    template_name = "crud/inventory_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        qs = super().get_queryset().select_related("product", "warehouse")
        allowed_sorts = {"-quantity", "quantity", "-updated", "updated"}
        sort = self.request.GET.get("sort")
        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_inventory = Inventory.objects.all()
        context["total_items"] = all_inventory.count()
        context["in_stock_count"] = all_inventory.filter(status="in_stock").count()
        context["low_stock_count"] = all_inventory.filter(status="low_stock").count()
        context["out_of_stock_count"] = all_inventory.filter(status="out_of_stock").count()
        context["discontinued_count"] = all_inventory.filter(status="discontinued").count()

        all_products = Product.objects.all()
        context["active_products_count"] = all_products.filter(status="active").count()
        context["draft_products_count"] = all_products.filter(status="draft").count()
        context["inactive_products_count"] = all_products.filter(status="inactive").count()

        context["current_sort"] = self.request.GET.get("sort", "-quantity")
        return context
class InventoryCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = "crud/inventory_form.html"
    success_url = reverse_lazy("crud:inventory_list")

    def form_valid(self, form):
        messages.success(self.request, f"Inventory created for “{form.instance.product.name}”.")
        return super().form_valid(form)


class InventoryUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = "crud/inventory_form.html"
    success_url = reverse_lazy("crud:inventory_list")

    def form_valid(self, form):
        messages.success(self.request, f"Inventory for “{form.instance.product.name}” updated.")
        return super().form_valid(form)


class InventoryDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Inventory
    template_name = "crud/inventory_confirm_delete.html"
    success_url = reverse_lazy("crud:inventory_list")

    def form_valid(self, form):
        messages.success(self.request, f"Inventory for “{self.object.product.name}” deleted.")
        return super().form_valid(form)



class InventoryBulkStockUpdateView(LoginRequiredMixin, View):
    """Handles the Bulk Stock Update modal (Step 2: Upload)."""
    template_name = "crud/inventory_bulk_stock_form.html"

    def get(self, request, *args, **kwargs):
        form = InventoryBulkStockUploadForm()
        html = render_to_string(self.template_name, {"form": form}, request=request)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"html": html})
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        form = InventoryBulkStockUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            html = render_to_string(self.template_name, {"form": form}, request=request)
            return JsonResponse({"success": False, "html": html})

        uploaded_file = request.FILES["file"]
        updated_count = 0
        skipped = 0

        try:
            decoded = uploaded_file.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(decoded))
            for row in reader:
                inv_id = row.get("Inventory ID") or row.get("id")
                qty = row.get("Quantity") or row.get("quantity")
                if not inv_id or qty in (None, ""):
                    skipped += 1
                    continue
                try:
                    inv = Inventory.objects.get(pk=int(inv_id))
                    inv.quantity = int(qty)
                    inv.save()
                    updated_count += 1
                except (Inventory.DoesNotExist, ValueError):
                    skipped += 1
        except Exception as e:
            form.add_error("file", f"File could not be processed: {e}")
            html = render_to_string(self.template_name, {"form": form}, request=request)
            return JsonResponse({"success": False, "html": html})

        msg = f"Bulk stock update complete — {updated_count} item(s) updated."
        if skipped:
            msg += f" {skipped} row(s) skipped."
        messages.success(request, msg)
        return JsonResponse({"success": True})


class InventoryBulkStockDownloadView(LoginRequiredMixin, View):
    """Handles Step 1: Download current stock as CSV."""

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="inventory_stock.csv"'
        writer = csv.writer(response)
        writer.writerow(["Inventory ID", "Product", "Warehouse", "Quantity", "Reorder Level", "Status"])
        for inv in Inventory.objects.select_related("product", "warehouse").all():
            writer.writerow([
                inv.id,
                inv.product.name,
                inv.warehouse.name if inv.warehouse else "",
                inv.quantity,
                inv.reorder_level,
                inv.get_status_display(),
            ])
        return response

# --- Catalog Uploads: full CRUD (tables2 + django-filter + crispy form + messages) ---
class CatalogUploadListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = CatalogUpload
    table_class = CatalogUploadTable
    filterset_class = CatalogUploadFilter
    template_name = "crud/catalogupload_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        qs = super().get_queryset()
        upload_type = self.request.GET.get("upload_type", "bulk")
        return qs.filter(upload_type=upload_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_uploads = CatalogUpload.objects.all()
        context["total_uploads"] = all_uploads.count()
        context["bulk_count"] = all_uploads.filter(upload_type="bulk").count()
        context["single_count"] = all_uploads.filter(upload_type="single").count()
        context["active_upload_type"] = self.request.GET.get("upload_type", "bulk")

        current_type_qs = all_uploads.filter(upload_type=context["active_upload_type"])
        context["action_required_count"] = current_type_qs.filter(status="pending").count()
        context["qc_progress_count"] = current_type_qs.filter(status="processing").count()
        context["qc_error_count"] = current_type_qs.filter(status="failed").count()
        context["qc_pass_count"] = current_type_qs.filter(status="completed").count()
        context["active_status_tab"] = self.request.GET.get("status", "")
        return context


class CatalogUploadCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = CatalogUpload
    form_class = CatalogUploadForm
    template_name = "crud/catalogupload_form.html"
    success_url = reverse_lazy("crud:catalogupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Catalog upload “{form.instance.file_name}” created.")
        return super().form_valid(form)


class CatalogUploadUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = CatalogUpload
    form_class = CatalogUploadForm
    template_name = "crud/catalogupload_form.html"
    success_url = reverse_lazy("crud:catalogupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Catalog upload “{form.instance.file_name}” updated.")
        return super().form_valid(form)


class CatalogUploadDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = CatalogUpload
    template_name = "crud/catalogupload_confirm_delete.html"
    success_url = reverse_lazy("crud:catalogupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Catalog upload “{self.object.file_name}” deleted.")
        return super().form_valid(form)


# --- Image Bulk Uploads: full CRUD (tables2 + django-filter + crispy form + messages) ---
class ImageBulkUploadListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = ImageBulkUpload
    table_class = ImageBulkUploadTable
    filterset_class = ImageBulkUploadFilter
    template_name = "crud/imagebulkupload_list.html"
    table_pagination = {"per_page": 10}


class ImageBulkUploadCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = ImageBulkUpload
    form_class = ImageBulkUploadForm
    template_name = "crud/imagebulkupload_form.html"
    success_url = reverse_lazy("crud:imagebulkupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Image bulk upload “{form.instance.name}” created.")
        return super().form_valid(form)


class ImageBulkUploadUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = ImageBulkUpload
    form_class = ImageBulkUploadForm
    template_name = "crud/imagebulkupload_form.html"
    success_url = reverse_lazy("crud:imagebulkupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Image bulk upload “{form.instance.name}” updated.")
        return super().form_valid(form)


class ImageBulkUploadDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = ImageBulkUpload
    template_name = "crud/imagebulkupload_confirm_delete.html"
    success_url = reverse_lazy("crud:imagebulkupload_list")

    def form_valid(self, form):
        messages.success(self.request, f"Image bulk upload “{self.object.name}” deleted.")
        return super().form_valid(form)


# --- Quality: full CRUD (tables2 + django-filter + crispy form + messages) ---
class QualityListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Quality
    table_class = QualityTable
    filterset_class = QualityFilter
    template_name = "crud/quality_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("product")


class QualityCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Quality
    form_class = QualityForm
    template_name = "crud/quality_form.html"
    success_url = reverse_lazy("crud:quality_list")

    def form_valid(self, form):
        messages.success(self.request, f"Quality check for “{form.instance.product.name}” created.")
        return super().form_valid(form)


class QualityUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Quality
    form_class = QualityForm
    template_name = "crud/quality_form.html"
    success_url = reverse_lazy("crud:quality_list")

    def form_valid(self, form):
        messages.success(self.request, f"Quality check for “{form.instance.product.name}” updated.")
        return super().form_valid(form)


class QualityDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Quality
    template_name = "crud/quality_confirm_delete.html"
    success_url = reverse_lazy("crud:quality_list")

    def form_valid(self, form):
        messages.success(self.request, f"Quality check for “{self.object.product.name}” deleted.")
        return super().form_valid(form)


# --- Products: full CRUD (tables2 + django-filter + crispy form + messages) ---
class ProductListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    filterset_class = ProductFilter
    template_name = "crud/product_list.html"
    table_pagination = {"per_page": 10}


class ProductCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "crud/product_form.html"
    success_url = reverse_lazy("crud:product_list")

    def form_valid(self, form):
        messages.success(self.request, f"Product “{form.instance.name}” created.")
        return super().form_valid(form)


class ProductUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "crud/product_form.html"
    success_url = reverse_lazy("crud:product_list")

    def form_valid(self, form):
        messages.success(self.request, f"Product “{form.instance.name}” updated.")
        return super().form_valid(form)


class ProductDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "crud/product_confirm_delete.html"
    success_url = reverse_lazy("crud:product_list")

    def form_valid(self, form):
        messages.success(self.request, f"Product “{self.object.name}” deleted.")
        return super().form_valid(form)


# --- Payments: full CRUD (tables2 + django-filter + crispy form + messages) ---
class PaymentListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Payment
    table_class = PaymentTable
    filterset_class = PaymentFilter
    template_name = "crud/payment_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("order")


class PaymentCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "crud/payment_form.html"
    success_url = reverse_lazy("crud:payment_list")

    def form_valid(self, form):
        messages.success(self.request, f"Payment created for order “{form.instance.order.order_number}”.")
        return super().form_valid(form)


class PaymentUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "crud/payment_form.html"
    success_url = reverse_lazy("crud:payment_list")

    def form_valid(self, form):
        messages.success(self.request, f"Payment for “{form.instance.order.order_number}” updated.")
        return super().form_valid(form)


class PaymentDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = "crud/payment_confirm_delete.html"
    success_url = reverse_lazy("crud:payment_list")

    def form_valid(self, form):
        messages.success(self.request, f"Payment for “{self.object.order.order_number}” deleted.")
        return super().form_valid(form)


# --- Warehouses: full CRUD (tables2 + django-filter + crispy form + messages) ---
class WarehouseListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Warehouse
    table_class = WarehouseTable
    filterset_class = WarehouseFilter
    template_name = "crud/warehouse_list.html"
    table_pagination = {"per_page": 10}


class WarehouseCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "crud/warehouse_form.html"
    success_url = reverse_lazy("crud:warehouse_list")

    def form_valid(self, form):
        messages.success(self.request, f"Warehouse “{form.instance.name}” created.")
        return super().form_valid(form)


class WarehouseUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "crud/warehouse_form.html"
    success_url = reverse_lazy("crud:warehouse_list")

    def form_valid(self, form):
        messages.success(self.request, f"Warehouse “{form.instance.name}” updated.")
        return super().form_valid(form)


class WarehouseDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Warehouse
    template_name = "crud/warehouse_confirm_delete.html"
    success_url = reverse_lazy("crud:warehouse_list")

    def form_valid(self, form):
        messages.success(self.request, f"Warehouse “{self.object.name}” deleted.")
        return super().form_valid(form)


# --- Influencer Campaigns: full CRUD (tables2 + django-filter + crispy form + messages) ---
class InfluencerCampaignListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = InfluencerCampaign
    table_class = InfluencerCampaignTable
    filterset_class = InfluencerCampaignFilter
    template_name = "crud/influencercampaign_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("product")


class InfluencerCampaignCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = InfluencerCampaign
    form_class = InfluencerCampaignForm
    template_name = "crud/influencercampaign_form.html"
    success_url = reverse_lazy("crud:influencercampaign_list")

    def form_valid(self, form):
        messages.success(self.request, f"Campaign “{form.instance.campaign_name}” created.")
        return super().form_valid(form)


class InfluencerCampaignUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = InfluencerCampaign
    form_class = InfluencerCampaignForm
    template_name = "crud/influencercampaign_form.html"
    success_url = reverse_lazy("crud:influencercampaign_list")

    def form_valid(self, form):
        messages.success(self.request, f"Campaign “{form.instance.campaign_name}” updated.")
        return super().form_valid(form)


class InfluencerCampaignDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = InfluencerCampaign
    template_name = "crud/influencercampaign_confirm_delete.html"
    success_url = reverse_lazy("crud:influencercampaign_list")

    def form_valid(self, form):
        messages.success(self.request, f"Campaign “{self.object.campaign_name}” deleted.")
        return super().form_valid(form)


# --- Advertisements: full CRUD (tables2 + django-filter + crispy form + messages) ---
class AdvertisementListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Advertisement
    table_class = AdvertisementTable
    filterset_class = AdvertisementFilter
    template_name = "crud/advertisement_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("product")


class AdvertisementCreateView(AjaxModalFormMixin, LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "crud/advertisement_form.html"
    success_url = reverse_lazy("crud:advertisement_list")

    def form_valid(self, form):
        messages.success(self.request, f"Advertisement “{form.instance.campaign_name}” created.")
        return super().form_valid(form)


class AdvertisementUpdateView(AjaxModalFormMixin, LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "crud/advertisement_form.html"
    success_url = reverse_lazy("crud:advertisement_list")

    def form_valid(self, form):
        messages.success(self.request, f"Advertisement “{form.instance.campaign_name}” updated.")
        return super().form_valid(form)


class AdvertisementDeleteView(AjaxModalDeleteMixin, LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = "crud/advertisement_confirm_delete.html"
    success_url = reverse_lazy("crud:advertisement_list")

    def form_valid(self, form):
        messages.success(self.request, f"Advertisement “{self.object.campaign_name}” deleted.")
        return super().form_valid(form)
from django.views.generic import TemplateView


class BarcodeScanView(LoginRequiredMixin, TemplateView):
    template_name = "crud/barcode_scan.html"
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect

class ReduceRTOReturnsView(LoginRequiredMixin, TemplateView):
    template_name = "crud/reduce_rto_returns.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["total_products"] = Product.objects.count()
        return context

    def post(self, request, *args, **kwargs):
        product_ids = request.POST.getlist("product_ids")
        if not product_ids:
            messages.warning(request, "No products selected.")
            return redirect("crud:reduce_rto_returns")

        applied_count = 0
        for pid in product_ids:
            prepaid_discount = request.POST.get(f"prepaid_discount_{pid}") or 0
            wdrp_discount = request.POST.get(f"wdrp_discount_{pid}") or 0
            try:
                product = Product.objects.get(pk=pid)
            except Product.DoesNotExist:
                continue

            discount_value = float(prepaid_discount) if float(prepaid_discount or 0) > 0 else float(wdrp_discount or 0)

            pricing, created = Pricing.objects.get_or_create(
                product=product,
                defaults={
                    "cost_price": product.price,
                    "selling_price": product.price,
                    "discount_percent": discount_value,
                    "status": "active",
                    "effective_date": timezone.now().date(),
                },
            )
            if not created:
                pricing.discount_percent = discount_value
                pricing.status = "active"
                pricing.save()
            applied_count += 1

        messages.success(request, f"Discount applied to {applied_count} product(s).")
        return redirect("crud:pricing_list")