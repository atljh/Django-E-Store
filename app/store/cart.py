from .models import Product
from django.contrib.auth.models import User
from .utils import *
from django.shortcuts import render, redirect


def cart_req(request):
    if User.is_authenticated:
        result = get_all_from_cart()
        products = Product.get_products_by_id([ids.get('_id') for ids in result])
        total_price = sum([price.price for price in products])
        quantity = [quant.get('quantity') for quant in result]
        items = zip(quantity, products)
        return render(request, 'cart.html', {'items': items, 'total_price': total_price})
    cart = request.session.get('cart')
    if not cart:
        return render(request, 'cart.html')
    quantity = reversed(list(cart.values()))
    products = Product.get_products_by_id(list(cart.keys()))
    items = zip(quantity, products)
    return render(request, 'cart.html', {'items': items})


def add_to_cart(request, product_id):
    if User.is_authenticated:
        if get_by_id(product_id):
            update_cart(product_id)
        else:
            write_cart(product_id)
    else:
        cart_data = request.session.get('cart', {})
        itm_count = cart_data.get(str(product_id), 0)
        cart_data[str(product_id)] = itm_count + 1
        request.session['cart'] = cart_data
    return redirect(f'/product/{product_id}')


def remove_from_cart(request, product_id):
    if User.is_authenticated:
        delete_from_cart(product_id)
        return redirect('/cart')
    cart = request.session.get('cart')
    if cart[str(product_id)] == 1:
        cart.pop(str(product_id))
    elif cart[str(product_id)] > 1:
        cart[str(product_id)] -= 1
    request.session['cart'] = cart
    return redirect('/cart')


def clear_cart(request):
    if User.is_authenticated:
        delete_cart()
        return redirect('/cart')
    request.session['cart'] = {}
    return redirect('/cart')
