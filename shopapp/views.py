from django.contrib.auth.models import Group
from django.shortcuts import render, reverse, redirect
from django.http import HttpRequest, HttpResponse
from timeit import default_timer
from django.urls import reverse

from shopapp.models import Product, Order
from .forms import ProductForm, OrderForm



# Create your views here.
def shop_index(request: HttpRequest):

    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 3000)
    ]

    pages = [
        ('products', 'products_list', 'View all products'),
        ('orders', 'orders_list', 'View all orders'),
        ('groups', 'groups_list', 'View all groups'),
        ('create orders', 'create_order', 'Create new orders'),
        ('create products', 'create_product', 'Create new products'),
    ]

    available_pages = []
    for page_name, url_name, description in pages:
        try:
            available_pages.append({
                'title': page_name,
                'url': reverse(f'shopapp:{url_name}'),
                'description': description,
            })
        except:
            pass

    context = {
        'time_running': default_timer(),
        'products': products,
        'available_pages': available_pages,
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }

    return render(request, 'shopapp/groups-list.html', context=context)

def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/product-list.html', context=context)

def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # description = form.cleaned_data['description']
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()

    context = {
        'form': form,
    }

    return render(request, 'shopapp/create-product.html', context=context)

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)

def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            products = form.cleaned_data['products']
            order.products.set(products)

            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'shopapp/create-order.html', context=context)