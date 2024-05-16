from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from .models import Order, OrderedItem
from products.models import Product

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')

    user = request.user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = None

    cart_order, created = Order.objects.get_or_create(
        owner=customer, 
        order_status=Order.CART_STAGE
    )
    ordered_items = cart_order.added_items.all()  # Access ordered items using related name
    context = {
        'cart_items': ordered_items,
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
            return redirect('profile')  # Redirect to a profile creation page

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
