from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user using Django's built-in authentication
        user = authenticate(request, username=username, password=password)

        # If the user is valid, log them in and redirect to the homepage
        if user is not None:
            login(request, user)
            return redirect('home')

        # If the user is not valid, display an error message
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    # If the request method is GET, just render the login page
    else:
        return render(request, 'store/login.html')


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products': products, 'carItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'carItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'carItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def updateItem(request):
    return render(request, 'store/index.html', context)


def index(request):
    return render(request, 'store/index.html')