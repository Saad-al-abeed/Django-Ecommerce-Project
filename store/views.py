from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):
    products = None
    category = None
    if (category_slug != None):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by("id")
    else:
        products = Product.objects.filter(is_available=True).order_by("id")
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = products.count()
    context = {
        "products" : paged_products,
        "count" : count,
        #"in_cart" : in_cart
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        product = Product.objects.get(category=category, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    context = {
        "product" : product,
        "in_cart" : in_cart
    }
    return render(request, "store/product_detail.html", context)
