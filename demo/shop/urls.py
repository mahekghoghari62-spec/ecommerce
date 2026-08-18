from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.shop_login, name="login"),
    path("register/", views.shop_register, name="register"),
    path("category/<str:category_key>/", views.category_detail, name="category"),
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
    path("checkout/success/", views.order_success_view, name="order_success"),

]