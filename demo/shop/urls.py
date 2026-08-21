from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.shop_login, name="login"),
    path("logout/", views.shop_logout, name="logout"),
    path("register/", views.shop_register, name="register"),
    path("category/<str:category_key>/", views.category_detail, name="category"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("profile/", views.profile_view, name="profile"),
    path("addresses/", views.address_list, name="address_list"),
    path("addresses/add/", views.address_add, name="address_add"),
    path("addresses/<int:pk>/edit/", views.address_edit, name="address_edit"),
    path("addresses/<int:pk>/delete/", views.address_delete, name="address_delete"),

    # Cart
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("cart/save-for-later/<int:item_id>/", views.save_for_later, name="save_for_later"),
    path("cart/move-to-cart/<int:item_id>/", views.move_to_cart, name="move_to_cart"),
    path("checkout/place-order/", views.place_order_view, name="place_order"),
    path("checkout/success/", views.order_success_view, name="order_success"),
    path("checkout/create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
    path("checkout/invoice/pdf/", views.invoice_pdf, name="invoice_pdf"),
    path("checkout/invoice/excel/", views.invoice_excel, name="invoice_excel"),
    path("product/<int:product_id>/review/", views.add_review, name="add_review"),
    path("policy/<slug:slug>/", views.policy_detail, name="policy_detail"),

    # Footer pages — each its own template/view
    path("about-us/", views.about_us, name="about_us"),
    path("contact-us/", views.contact_us, name="contact_us"),
    path("careers/", views.careers, name="careers"),
    path("myshop-stories/", views.myshop_stories, name="myshop_stories"),
    path("press/", views.press, name="press"),
    path("corporate-information/", views.corporate_information, name="corporate_information"),
    path("payments/", views.payments, name="payments"),
    path("faq/", views.faq, name="faq"),
    path("sitemap/", views.sitemap, name="sitemap"),
    path("grievance-redressal/", views.grievance_redressal, name="grievance_redressal"),
    path("advertise/", views.advertise, name="advertise"),
    path("gift-cards/", views.gift_cards, name="gift_cards"),
    path("help-center/", views.help_center, name="help_center"),
]