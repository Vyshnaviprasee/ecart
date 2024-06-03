from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customers.models import *
from .models import Order, OrderedItem
from products.models import Product
import logging

logger = logging.getLogger('django')


def cart(request):
    user = request.user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        messages.error(request, "Please create your customer profile.")
        return redirect('show_accounts')

    cart_order, created = Order.objects.get_or_create(
        owner=customer, 
        order_status=Order.CART_STAGE
    )
    ordered_items = cart_order.added_items.all()
    subtotal = sum(item.product.price * item.quantity for item in ordered_items)
    shipping_fee = 100.00
    total_price = subtotal + shipping_fee
    
    context = {
        'cart_items': ordered_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        user = request.user

        try:
            customer = user.customer
        except Customer.DoesNotExist:
            messages.error(request, "Please create your customer profile.")
            return redirect('show_accounts')

        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, pk=pk)

        cart_order, created = Order.objects.get_or_create(
            owner=customer, 
            order_status=Order.CART_STAGE,
        )

        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_order,
        )
        if created:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity
        ordered_item.save()
        messages.success(request, "Product added to cart successfully.")
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    user = request.user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        messages.error(request, "Please create your customer profile.")
        return redirect('profile')

    product = get_object_or_404(Product, pk=pk)
    cart_order = get_object_or_404(
        Order, 
        owner=customer, 
        order_status=Order.CART_STAGE
        )
    ordered_item = get_object_or_404(
        OrderedItem, 
        product=product, 
        owner=cart_order
        )

    ordered_item.delete()
    messages.success(request, "Product removed from cart successfully.")
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user

        customer = get_customer(user)
        if not customer:
            return redirect('cart')

        order_obj, total_price = get_order_and_price(request, customer)
        if not order_obj:
            return redirect('cart')

        if confirm_order(order_obj, total_price):
            messages.success(request, "Order confirmed successfully.")
        else:
            messages.error(request, "Something went wrong. Please try again.")

    return redirect('index')

def get_customer(user):
    try:
        return user.customer
    except Customer.DoesNotExist:
        logger.error("Customer profile does not exist")
        messages.error(user.request, "Please create your customer profile.")
        return None

def get_order_and_price(request, customer):
    try:
        total_price = float(request.POST.get('total_price'))
        order_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)
        return order_obj, total_price
    except (Order.DoesNotExist, ValueError):
        logger.error("No active cart found or invalid total price")
        messages.error(request, "No active cart found or invalid total price.")
        return None, None

def confirm_order(order_obj, total_price):
    try:
        order_obj.order_status = Order.ORDER_CONFIRMED
        order_obj.total_price = total_price
        order_obj.save()
        logger.debug("Order confirmed and saved successfully")
        return True
    except Exception as e: #if there is an error
        logger.error(f"Unexpected error during checkout: {e}", exc_info=True) #log the error with exc_info=True
        return False

@login_required(login_url='login')
def show_orders(request):
    user = request.user
    customer = user.customer
    all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context = {
        'all_orders': all_orders
    }
    return render(request, 'orders.html', context)

