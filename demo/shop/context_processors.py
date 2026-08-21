"""
shop/context_processors.py

IMPORTANT: this file must contain BOTH of these — your settings.py already
registers `shop.context_processors.cart_count` (that's what powers the cart
badge count in the header), and now also `shop.context_processors.default_address`
for the delivery-location text. Don't replace one with the other; keep both
functions in this single file.
"""


def cart_count(request):
    cart = request.session.get("cart", {})
    return {"cart_item_count": sum(cart.values())}


def default_address(request):
    if not request.user.is_authenticated:
        return {"default_address": None}

    address = request.user.addresses.filter(is_default=True).first()
    if not address:
        address = request.user.addresses.first()

    return {"default_address": address}