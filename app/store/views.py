from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Order, SubCategory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import *
from . import cart as cart_view


def product_list(request):
    search_result = request.GET.get('search')
    ctgry = request.GET.get('category', 'all')
    min_price = request.GET.get('min', 0)
    max_price = request.GET.get('max', 9999999999)
    if search_result:
        items = Product.objects.filter(name__contains=search_result.capitalize())
    else:
        items = Product.get_with_filters(ctgry, min_price, max_price).order_by("-date_created")
    categories = Category.get_all_categories()
    paginator = Paginator(items, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(items)
    return render(request, 'main.html', {'items': items, 'categories': categories, 'page_obj': page_obj})


def product_req(request, product_id):
    item = Product.objects.get(id=product_id)
    return render(request, 'product.html', {'item': item})


def category_req(request, category_id):
    subcategories = SubCategory.get_subcategories(category_id)
    category_name = Category.get_category_by_id(category_id)
    return render(request, 'category.html', {'subcategories': subcategories, 'category_name': category_name})


def subcategory_req(request, subcategory_id):
    items = Product.get_all_subcategoryid(subcategory_id)
    return render(request, 'subcategory.html', {'items': items})


def categories_req(request):
    categories = Category.get_all_categories()
    return render(request, 'categories.html', {'categories': categories})


def cabinet_req(request):
    return render(request, 'cabinet.html')


def orders_req(request):
    Order.get_orders_by_customer(request.user.id)
    orders = Order.get_orders_by_customer(request.user.id)
    return render(request, 'orders.html', {'orders': orders})


@login_required(login_url='login')
def checkout_req(request):
    return render(request, 'checkout.html')


def save_order(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    if User.is_authenticated:
        customer = request.user
        result = get_all_from_cart()
        products = Product.get_products_by_id([ids.get('_id') for ids in result])
    else:
        customer = None
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

    def get_quantity(product):
        if User.is_authenticated:
            return get_by_id(product.id).get('quantity')
        else:
            cart = request.session.get('cart')
            return cart.get(str(product.id))

    for product in products:
        order = Order(customer=customer,
                      name=name,
                      surname=surname,
                      email=email,
                      product=product,
                      price=product.price,
                      address=address,
                      phone=phone,
                      quantity=get_quantity(product))
        order.save()
    cart_view.clear_cart(request)
    return render(request, 'save_order.html')
