from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # current_user = request.user # COMMENTED OUT FOR TESTING
    product = Product.objects.get(id=product_id)

    # --- COMMENTED OUT VARIATION LOGIC START ---
    # product_variation = []
    # if request.method == 'POST':
    #     for item in request.POST:
    #         key = item
    #         value = request.POST[key]
    #         try:
    #             variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
    #             product_variation.append(variation)
    #         except:
    #             pass
    # --- COMMENTED OUT VARIATION LOGIC END ---

    # --- COMMENTED OUT USER AUTH LOGIC START ---
    # if current_user.is_authenticated:
    #    # [Original logic for authenticated users was here]
    #    pass
    # else:
    # --- COMMENTED OUT USER AUTH LOGIC END ---

    # SIMPLIFIED LOGIC FOR TESTING (Session based only, no variations)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        # We look for the cart item matching the product and the cart
        # We removed the variation check here
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()

    # --- COMMENTED OUT VARIATION SAVING ---
    # if len(product_variation) > 0:
    #     cart_item.variations.clear()
    #     cart_item.variations.add(*product_variation)
    # cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        # --- COMMENTED OUT USER LOGIC ---
        # if request.user.is_authenticated:
        #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        # else:

        # TESTING LOGIC: Always use session cart
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    # --- COMMENTED OUT USER LOGIC ---
    # if request.user.is_authenticated:
    #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    # else:

    # TESTING LOGIC: Always use session cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        # --- COMMENTED OUT USER LOGIC ---
        # if request.user.is_authenticated:
        #     cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        # else:

        # TESTING LOGIC: Always use session cart
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100 # 2 % tax
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


# You may want to remove @login_required for full testing,
# but keeping it here as the view logic itself is what was requested to be changed.
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        # --- COMMENTED OUT USER LOGIC ---
        # if request.user.is_authenticated:
        #     cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        # else:

        # TESTING LOGIC: Always use session cart
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
