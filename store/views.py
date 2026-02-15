from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    products = None
    category = None
    if (category_slug != None):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    count = products.count()
    context = {
        "products" : products,
        "count" : count
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        product = Product.objects.get(category=category, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        "product" : product
    }
    return render(request, "store/product_detail.html", context)
