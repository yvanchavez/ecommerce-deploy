import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import datetime
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from .forms import RegistrarForm, PasswordResetForm
from .models import *

from django.views.generic.list import ListView

from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'store/store.html', context)


def search(request):
    categoria_all = request.GET['category']
    if  categoria_all == '0':
        query = request.GET['q']
        results = Product.objects.filter(name__icontains=query)

    elif 'q' in request.GET:
        # Get the selected category id
        sel_category = request.GET.get('category', None)
        # If it exists, get the category object
        if sel_category:
            category = get_object_or_404(Category, pk=sel_category)
        query = request.GET['q']
        results = Product.objects.filter(name__icontains=query)
        # If category objects exists filter the result set based on that
        if category:
            results = results.filter(categories__name__icontains=category.name)
    #   print results.query
    else:
        query = ""
        results = None
    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'query': query, 'products': results, 'categories': categories, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def filterCategories(request):
    ### Get the categories without any parent.
    q = request.GET['q']
    categories = Category.objects.filter(parent=None).order_by('name')
    context = {'kategorie': kategorie}
    return render(request, 'ogloszenia/index.html', context=context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def detail(request, id):
    data = cartData(request)

    cartItems = data['cartItems']

    product = Product.objects.get(id=id)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/detail.html', context)


def perfil(request):
    template_name = 'store/perfil.html'
    orders = Order.objects.filter(customer=request.user.customer)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {"orders": orders, 'cartItems': cartItems}
    return render(request, template_name, context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'].replace(',', '.'))
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            direccion=data['shipping']['direccion'],
            provincia=data['shipping']['provincia'],
            distrito=data['shipping']['distrito'],
        )
    return JsonResponse('Payment submitted..', safe=False)


def registrate(request):
    template_name = 'store/registrate.html'
    if request.method == 'POST':
        form = RegistrarForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            customer = Customer.objects.create(user=user)
            customer.email = form.cleaned_data['email']
            customer.name = user.username
            customer.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrarForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def change_password(request):
    template_name = 'store/change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


def password_reset(request):
    template_name = 'store/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'store/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class ProductView(ListView):
    model = Product
    template_name = 'store/productos.html'
    paginate_by = 6


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'store/product_create.html'
    fields = ['name', 'price', 'categories', 'image1', 'image2']

    def get_success_url(self):
        return reverse('products')


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/productdetail.html'


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'store/product_create.html'
    fields = ['name', 'price', 'categories', 'image1', 'image2']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # controla si el usuario edita o crea
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse('products')


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products')
    template_name = 'store/confirm_product_deletion.html'
