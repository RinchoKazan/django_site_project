from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from timeit import default_timer
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order



# Create your views here.
class ShopIndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:

        pages = [
            ('products', 'products_list', 'View all products'),
            ('orders', 'orders_list', 'View all orders'),
            ('groups', 'groups_list', 'View all groups'),
            ('create products', 'product_create', 'Create new products'),
            ('create orders', 'order_create', 'Create new orders'),
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
            'products': Product.objects.all(),
            'available_pages': available_pages,
        }

        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'


class ProductsListView(ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductCreateView(CreateView):
    # template_name = 'shopapp/create-product.html'
    # fields = ['name', 'price', 'description', 'discount']

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    # template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    def form_valid(self, form):
        succes_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(succes_url)



class OrdersListView(ListView):
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrdersDetailsView(DetailView):
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrderCreateView(CreateView):
    # template_name = 'shopapp/create-order.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shopapp:orders_list')

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    # template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse(
            'shopapp:orders_details',
            kwargs={'pk': self.object.pk}
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse('shopapp:orders_list')
#             return redirect(url)
#     else:
#         form = OrderForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-order.html', context=context)




# def orders_list(request: HttpRequest):
#     context = {
#         'orders': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, 'shopapp/order_list.html', context=context)


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse('shopapp:products_list')
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)

# def products_list(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#
#     }
#     return render(request, 'shopapp/product_list.html', context=context)


# def shop_index(request: HttpRequest):
#
#     products = [
#         ('Laptop', 1999),
#         ('Desktop', 2999),
#         ('smartphone', 3000),
#     ]
#
#     pages = [
#         ('products', 'products_list', 'View all products'),
#         ('orders', 'orders_list', 'View all orders'),
#         ('groups', 'groups_list', 'View all groups'),
#         ('create products', 'create_product', 'Create new products'),
#         ('create orders', 'create_order', 'Create new orders'),
#     ]
#     available_pages = []
#     for page_name, url_name, description in pages:
#         try:
#             available_pages.append({
#                 'title': page_name,
#                 'url': reverse(f'shopapp:{url_name}'),
#                 'description': description,
#             })
#         except:
#             pass
#
#     context = {
#         'time_running': default_timer(),
#         'products': products,
#         'available_pages': available_pages,
#     }
#
#
#     return render(request, 'shopapp/shop-index.html', context=context)


# def groups_list(request: HttpRequest):
#     context = {
#         'groups': Group.objects.prefetch_related('permissions').all(),
#     }
#     return render(request, 'shopapp/groups-list.html', context=context)
