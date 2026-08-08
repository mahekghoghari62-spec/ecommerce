from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from .mixins import AjaxModalDeleteMixin, AjaxModalFormMixin

from .filters import CatalogUploadFilter, ClaimFilter, ContactFilter, ImageBulkUploadFilter, InventoryFilter, OrderFilter, PricingFilter, ProductFilter, ProjectFilter, QualityFilter, ReturnFilter
from .forms import CatalogUploadForm, ClaimForm, ContactForm, ImageBulkUploadForm, InventoryForm, OrderForm, PricingForm, ProductForm, QualityForm, ReturnForm
from .models import CatalogUpload, Claim, Contact, ImageBulkUpload, Inventory, Order, Pricing, Product, Project, Quality, Return
from .tables import CatalogUploadTable, ClaimTable, ContactTable, ImageBulkUploadTable, InventoryTable, OrderTable, PricingTable, ProductTable, ProjectTable, QualityTable, ReturnTable

# --- Orders: full CRUD (tables2 + django-filter + crispy form + messages) ---
class OrderListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = "crud/order_list.html"
    table_pagination = {"per_page": 10}


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


# --- Inventory: full CRUD (tables2 + django-filter + crispy form + messages) ---
class InventoryListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Inventory
    table_class = InventoryTable
    filterset_class = InventoryFilter
    template_name = "crud/inventory_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("product")


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


# --- Catalog Uploads: full CRUD (tables2 + django-filter + crispy form + messages) ---
class CatalogUploadListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = CatalogUpload
    table_class = CatalogUploadTable
    filterset_class = CatalogUploadFilter
    template_name = "crud/catalogupload_list.html"
    table_pagination = {"per_page": 10}


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