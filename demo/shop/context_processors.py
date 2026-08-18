def cart_count(request):
    """Adds `cart_item_count` to every template context (used in navbar)."""
    if request.user.is_authenticated:
        cart = getattr(request.user, "cart", None)
        if cart:
            return {"cart_item_count": cart.total_items}
    return {"cart_item_count": 0}