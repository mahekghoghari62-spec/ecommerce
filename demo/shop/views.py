from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.views.decorators.http import require_POST
import razorpay
from crud.models import Product as CrudProduct, Order as CrudOrder, Payment as CrudPayment
from .forms import AddressForm, ProfileForm, CustomerRegistrationForm
from .models import Address, CustomerProfile
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


CATEGORY_ICONS = {
    "electronics": "bi-laptop",
    "fashion": "bi-bag-fill",
    "home": "bi-house-door-fill",
    "beauty": "bi-brush",
    "grocery": "bi-basket3-fill",
    "other": "bi-grid-3x3-gap-fill",
}


def get_nav_categories():
    active_keys = (
        CrudProduct.objects.filter(status="active")
        .values_list("category", flat=True)
        .distinct()
    )
    return [
        (key, label, CATEGORY_ICONS.get(key, "bi-grid"))
        for key, label in CrudProduct.CATEGORY_CHOICES
        if key in active_keys
    ]


def home(request):
    products = CrudProduct.objects.filter(status="active").order_by("-created")[:12]
    return render(request, "shop/home.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "products": products,
        "cart_map": request.session.get("cart", {}),
    })


def category_detail(request, category_key):
    label = dict(CrudProduct.CATEGORY_CHOICES).get(category_key, category_key)
    products = CrudProduct.objects.filter(status="active", category=category_key).order_by("-created")
    return render(request, "shop/category.html", {
        "nav_categories": get_nav_categories(),
        "current_category": category_key,
        "category_label": label,
        "products": products,
        "cart_map": request.session.get("cart", {}),
    })


@login_required
def profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("shop:profile")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "shop/profile.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "form": form,
    })


@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    return render(request, "shop/address_list.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "addresses": addresses,
    })


@login_required
def address_add(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                request.user.addresses.update(is_default=False)
            address.save()
            messages.success(request, "Address added.")
            return redirect("shop:address_list")
    else:
        form = AddressForm()
    return render(request, "shop/address_form.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "form": form,
        "title": "Add Address",
    })


@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.is_default:
                request.user.addresses.exclude(pk=address.pk).update(is_default=False)
            updated.save()
            messages.success(request, "Address updated.")
            return redirect("shop:address_list")
    else:
        form = AddressForm(instance=address)
    return render(request, "shop/address_form.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "form": form,
        "title": "Edit Address",
    })


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address deleted.")
        return redirect("shop:address_list")
    return render(request, "shop/address_confirm_delete.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "address": address,
    })


def shop_login(request):
    next_url = request.GET.get("next") or "shop:home"

    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get("next") or next_url)
    else:
        form = AuthenticationForm()

    return render(request, "shop/login.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "form": form,
        "next": next_url,
    })


def shop_register(request):
    next_url = request.GET.get("next") or "shop:home"

    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(request.POST.get("next") or next_url)
    else:
        form = CustomerRegistrationForm()

    return render(request, "shop/register.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "form": form,
        "next": next_url,
    })


# ---------------------------
# Cart views
# ---------------------------

def _get_price(product):
    """Handle either .price or .selling_price depending on the model."""
    return getattr(product, "price", None) or getattr(product, "selling_price", 0)


def cart_view(request):
    cart = request.session.get("cart", {})
    active_items = []
    subtotal = 0
    total_items = 0

    for product_id, qty in cart.items():
        product = CrudProduct.objects.filter(id=product_id).first()
        if product:
            price = _get_price(product)
            line_total = price * qty
            subtotal += line_total
            total_items += qty
            active_items.append({
                "id": product_id,
                "product": product,
                "quantity": qty,
                "line_total": line_total,
            })

    saved = request.session.get("saved_for_later", {})
    saved_items = []
    for product_id in saved:
        product = CrudProduct.objects.filter(id=product_id).first()
        if product:
            saved_items.append({"id": product_id, "product": product})

    related_products = CrudProduct.objects.filter(status="active").exclude(
        id__in=list(cart.keys()) + list(saved.keys())
    ).order_by("-created")[:6]

    return render(request, "shop/cart.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "active_items": active_items,
        "saved_items": saved_items,
        "related_products": related_products,
        "total_items": total_items,
        "subtotal": subtotal,
        "delivery_date": timezone.now() + timedelta(days=5),
    })


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def add_to_cart(request, product_id):
    product = get_object_or_404(CrudProduct, id=product_id)
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    request.session.modified = True

    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "message": f"{product.name} added to cart.",
            "quantity": cart[str(product_id)],
            "cart_count": sum(cart.values()),
        })

    messages.success(request, f"{product.name} added to cart.")
    next_url = request.POST.get("next")
    return redirect(next_url or "shop:cart")


def update_cart_item(request, item_id):
    cart = request.session.get("cart", {})
    item_id = str(item_id)
    action = request.POST.get("action")
    removed = False
    qty = cart.get(item_id, 0)

    if item_id in cart:
        if action == "increase":
            cart[item_id] += 1
            qty = cart[item_id]
        elif action == "decrease":
            cart[item_id] -= 1
            if cart[item_id] <= 0:
                cart.pop(item_id, None)
                qty = 0
                removed = True
            else:
                qty = cart[item_id]
        request.session["cart"] = cart
        request.session.modified = True

    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "quantity": qty,
            "removed": removed,
            "cart_count": sum(cart.values()),
        })

    return redirect("shop:cart")


def remove_cart_item(request, item_id):
    cart = request.session.get("cart", {})
    cart.pop(str(item_id), None)
    request.session["cart"] = cart
    messages.success(request, "Item removed from cart.")
    return redirect("shop:cart")


def save_for_later(request, item_id):
    cart = request.session.get("cart", {})
    saved = request.session.get("saved_for_later", {})
    if str(item_id) in cart:
        saved[str(item_id)] = cart.pop(str(item_id))
        request.session["cart"] = cart
        request.session["saved_for_later"] = saved
    return redirect("shop:cart")


def move_to_cart(request, item_id):
    cart = request.session.get("cart", {})
    saved = request.session.get("saved_for_later", {})
    if str(item_id) in saved:
        cart[str(item_id)] = saved.pop(str(item_id))
        request.session["cart"] = cart
        request.session["saved_for_later"] = saved
    return redirect("shop:cart")


# ---------------------------
# Checkout / Place Order / Razorpay
# ---------------------------

@login_required
def place_order_view(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:cart")

    addresses = request.user.addresses.all()
    active_items = []
    subtotal = 0

    for product_id, qty in cart.items():
        product = CrudProduct.objects.filter(id=product_id).first()
        if product:
            price = _get_price(product)
            line_total = price * qty
            subtotal += line_total
            active_items.append({
                "product": product,
                "quantity": qty,
                "line_total": line_total,
            })

    PAYMENT_METHOD_MAP = {
        "cod": "cash",
        "upi": "upi",
        "card": "card",
    }

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        payment_choice = request.POST.get("payment_method")

        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect("shop:place_order")

        if payment_choice not in PAYMENT_METHOD_MAP:
            messages.error(request, "Please select a payment method.")
            return redirect("shop:place_order")

        address = get_object_or_404(Address, pk=address_id, user=request.user)
        payment_method = PAYMENT_METHOD_MAP[payment_choice]

        razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
        razorpay_order_id = request.POST.get("razorpay_order_id", "")
        razorpay_signature = request.POST.get("razorpay_signature", "")

        if payment_choice in ("upi", "card"):
            if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect("shop:place_order")

            client = get_razorpay_client()
            try:
                client.utility.verify_payment_signature({
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                })
            except razorpay.errors.SignatureVerificationError:
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect("shop:place_order")

            payment_status = "completed"
            transaction_id = razorpay_payment_id
        else:
            payment_status = "pending"
            transaction_id = ""

        for product_id, qty in cart.items():
            product = CrudProduct.objects.filter(id=product_id).first()
            if not product:
                continue
            price = _get_price(product)
            line_amount = price * qty

            order = CrudOrder.objects.create(
                customer_name=request.user.get_full_name() or request.user.username,
                customer_email=request.user.email,
                product=product,
                quantity=qty,
                amount=line_amount,
                status="pending",
            )

            CrudPayment.objects.create(
                order=order,
                amount=line_amount,
                method=payment_method,
                status=payment_status,
                transaction_id=transaction_id,
                notes=f"Payment via {payment_choice.upper()} (checkout)",
            )

        request.session["cart"] = {}
        request.session.modified = True

        messages.success(request, "Your order has been placed successfully!")
        return redirect("shop:order_success")

    return render(request, "shop/place_order.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
        "addresses": addresses,
        "active_items": active_items,
        "subtotal": subtotal,
    })


@login_required
@require_POST
def create_razorpay_order(request):
    cart = request.session.get("cart", {})
    if not cart:
        return JsonResponse({"success": False, "error": "Cart is empty."})

    subtotal = 0
    for product_id, qty in cart.items():
        product = CrudProduct.objects.filter(id=product_id).first()
        if product:
            price = _get_price(product)
            subtotal += price * qty

    amount_paise = int(subtotal * 100)

    client = get_razorpay_client()
    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1,
    })

    return JsonResponse({
        "success": True,
        "order_id": razorpay_order["id"],
        "amount": amount_paise,
        "key": settings.RAZORPAY_KEY_ID,
        "name": request.user.get_full_name() or request.user.username,
        "email": request.user.email,
    })


@login_required
def order_success_view(request):
    return render(request, "shop/order_success.html", {
        "nav_categories": get_nav_categories(),
        "current_category": None,
    })