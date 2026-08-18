from django.urls import path

from . import views

app_name = "crud"

urlpatterns = [
    # Orders (full CRUD)
    path("orders/", views.OrderListView.as_view(), name="order_list"),
    path("orders/new/", views.OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/edit/", views.OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),
    path("barcode-scan/", views.BarcodeScanView.as_view(), name="barcode_scan"),

    # Contacts (full CRUD)
    path("contacts/", views.ContactListView.as_view(), name="contact_list"),
    path("contacts/new/", views.ContactCreateView.as_view(), name="contact_create"),
    path("contacts/<int:pk>/edit/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contacts/<int:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),

    # Projects (relational list + detail)
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),

    # Returns (full CRUD)
    path("returns/", views.ReturnListView.as_view(), name="return_list"),
    path("returns/new/", views.ReturnCreateView.as_view(), name="return_create"),
    path("returns/<int:pk>/edit/", views.ReturnUpdateView.as_view(), name="return_update"),
    path("returns/<int:pk>/delete/", views.ReturnDeleteView.as_view(), name="return_delete"),

    # Pricing (full CRUD)
    path("pricing/", views.PricingListView.as_view(), name="pricing_list"),
    path("pricing/new/", views.PricingCreateView.as_view(), name="pricing_create"),
    path("pricing/<int:pk>/edit/", views.PricingUpdateView.as_view(), name="pricing_update"),
    path("pricing/<int:pk>/delete/", views.PricingDeleteView.as_view(), name="pricing_delete"),
    path("pricing/reduce-rto-returns/", views.ReduceRTOReturnsView.as_view(), name="reduce_rto_returns"),

    # Claims (full CRUD)
    path("claims/", views.ClaimListView.as_view(), name="claim_list"),
    path("claims/new/", views.ClaimCreateView.as_view(), name="claim_create"),
    path("claims/<int:pk>/edit/", views.ClaimUpdateView.as_view(), name="claim_update"),
    path("claims/<int:pk>/delete/", views.ClaimDeleteView.as_view(), name="claim_delete"),

    # Support (shared: Help + My Tickets)
    path("support/", views.SupportView.as_view(), name="support"),

    # Inventory (full CRUD)
    path("inventory/", views.InventoryListView.as_view(), name="inventory_list"),
    path("inventory/new/", views.InventoryCreateView.as_view(), name="inventory_create"),
    path("inventory/<int:pk>/edit/", views.InventoryUpdateView.as_view(), name="inventory_update"),
    path("inventory/<int:pk>/delete/", views.InventoryDeleteView.as_view(), name="inventory_delete"),
    path("inventory/bulk-stock/", views.InventoryBulkStockUpdateView.as_view(), name="inventory_bulk_stock_modal"),
    path("inventory/bulk-stock/download/", views.InventoryBulkStockDownloadView.as_view(), name="inventory_bulk_stock_download"),
    path("inventory/blocked/", views.BlockedProductsView.as_view(), name="blocked_products"),

    # Catalog Uploads (full CRUD)
    path("catalog-uploads/", views.CatalogUploadListView.as_view(), name="catalogupload_list"),
    path("catalog-uploads/new/", views.CatalogUploadCreateView.as_view(), name="catalogupload_create"),
    path("catalog-uploads/<int:pk>/edit/", views.CatalogUploadUpdateView.as_view(), name="catalogupload_update"),
    path("catalog-uploads/<int:pk>/delete/", views.CatalogUploadDeleteView.as_view(), name="catalogupload_delete"),
    path("catalog-uploads/bulk/categories/", views.BulkCatalogCategoryView.as_view(), name="bulk_catalog_categories"),

    # Image Bulk Uploads (full CRUD)
    path("image-bulk-uploads/", views.ImageBulkUploadPageView.as_view(), name="imagebulkupload_list"),
    path("image-bulk-uploads/records/", views.ImageBulkUploadListView.as_view(), name="imagebulkupload_records"),
    path("image-bulk-uploads/new/", views.ImageBulkUploadCreateView.as_view(), name="imagebulkupload_create"),
    path("image-bulk-uploads/<int:pk>/edit/", views.ImageBulkUploadUpdateView.as_view(), name="imagebulkupload_update"),
    path("image-bulk-uploads/<int:pk>/delete/", views.ImageBulkUploadDeleteView.as_view(), name="imagebulkupload_delete"),

    # Quality (full CRUD)
    path("quality/", views.QualityDashboardView.as_view(), name="quality_list"),
    path("quality/records/", views.QualityListView.as_view(), name="quality_records"),
    path("quality/new/", views.QualityCreateView.as_view(), name="quality_create"),
    path("quality/<int:pk>/edit/", views.QualityUpdateView.as_view(), name="quality_update"),
    path("quality/<int:pk>/delete/", views.QualityDeleteView.as_view(), name="quality_delete"),

    # Products (full CRUD)
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/new/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),

    # Payments (full CRUD)
    path("payments/", views.PaymentListView.as_view(), name="payment_list"),
    path("payments/new/", views.PaymentCreateView.as_view(), name="payment_create"),
    path("payments/<int:pk>/edit/", views.PaymentUpdateView.as_view(), name="payment_update"),
    path("payments/<int:pk>/delete/", views.PaymentDeleteView.as_view(), name="payment_delete"),
    path("payments/help/", views.PaymentsHelpView.as_view(), name="payments_help"),
    path("payments/help/my-tickets/", views.PaymentsMyTicketsView.as_view(), name="payments_my_tickets"),
    path("payments/help/<str:slug>/", views.PaymentsHelpDetailView.as_view(), name="payments_help_detail"),

    # Warehouses (full CRUD)
    path("warehouses/", views.WarehouseListView.as_view(), name="warehouse_list"),
    path("warehouses/new/", views.WarehouseCreateView.as_view(), name="warehouse_create"),
    path("warehouses/<int:pk>/edit/", views.WarehouseUpdateView.as_view(), name="warehouse_update"),
    path("warehouses/<int:pk>/delete/", views.WarehouseDeleteView.as_view(), name="warehouse_delete"),
    path("warehouse/request-callback/", views.CallbackRequestCreateView.as_view(), name="callbackrequest_create"),

    # Influencer Campaigns (full CRUD)
    path("influencer-campaigns/", views.InfluencerMarketingDashboardView.as_view(), name="influencercampaign_list"),
    path("influencer-campaigns/records/", views.InfluencerCampaignListView.as_view(), name="influencercampaign_records"),
    path("influencer-campaigns/new/", views.InfluencerCampaignCreateView.as_view(), name="influencercampaign_create"),
    path("influencer-campaigns/<int:pk>/edit/", views.InfluencerCampaignUpdateView.as_view(), name="influencercampaign_update"),
    path("influencer-campaigns/<int:pk>/delete/", views.InfluencerCampaignDeleteView.as_view(), name="influencercampaign_delete"),
    path("influencer-campaigns/select-catalogs/", views.InfluencerSelectCatalogsView.as_view(), name="influencer_select_catalogs"),

    # Advertisements (full CRUD)
    path("advertisements/", views.AdvertisementDashboardView.as_view(), name="advertisement_list"),
    path("advertisements/records/", views.AdvertisementListView.as_view(), name="advertisement_records"),
    path("advertisements/new/", views.AdvertisementCreateView.as_view(), name="advertisement_create"),
    path("advertisements/<int:pk>/edit/", views.AdvertisementUpdateView.as_view(), name="advertisement_update"),
    path("advertisements/<int:pk>/delete/", views.AdvertisementDeleteView.as_view(), name="advertisement_delete"),

    # Promotions (full CRUD)
    path("promotions/", views.PromotionListView.as_view(), name="promotion_list"),
    path("promotions/new/", views.PromotionCreateView.as_view(), name="promotion_create"),
    path("promotions/<int:pk>/edit/", views.PromotionUpdateView.as_view(), name="promotion_update"),
    path("promotions/<int:pk>/delete/", views.PromotionDeleteView.as_view(), name="promotion_delete"),

    path("instant-cash/", views.InstantCashView.as_view(), name="instant_cash"),
    path("instant-cash/help/", views.InstantCashHelpView.as_view(), name="instant_cash_help"),
    path("business-dashboard/", views.BusinessDashboardView.as_view(), name="business_dashboard"),
    # Store Reports
    path("reports/", views.StoreReportsView.as_view(), name="store_reports"),
    path("reports/sales/excel/", views.SalesReportExcelView.as_view(), name="sales_report_excel"),
    path("reports/sales/pdf/", views.SalesReportPDFView.as_view(), name="sales_report_pdf"),
    path("reports/visitors/excel/", views.VisitorsReportExcelView.as_view(), name="visitors_report_excel"),
    path("reports/visitors/pdf/", views.VisitorsReportPDFView.as_view(), name="visitors_report_pdf"),
    path("settings/", views.SettingsView.as_view(), name="settings"),

    # Panel Users (full CRUD)
    path("users/", views.PanelUserListView.as_view(), name="paneluser_list"),
    path("users/new/", views.PanelUserCreateView.as_view(), name="paneluser_create"),
    path("users/<int:pk>/edit/", views.PanelUserUpdateView.as_view(), name="paneluser_update"),
    path("users/<int:pk>/delete/", views.PanelUserDeleteView.as_view(), name="paneluser_delete"),
]