from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from products.models import Product

# Create your models here.

class Order(models.Model):
    LIVE = 1
    DELETE = 0
    ITEM_STATUS_CHOICES = (
        (LIVE, "Live"),
        (DELETE, "Delete"),
    )

    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    ORDER_COMPLETED = 5
    ORDER_STATUS_CHOICES = (
        (CART_STAGE, "Cart"),
        (ORDER_CONFIRMED, "Order Confirmed"),
        (ORDER_PROCESSED, "Order Processed"),
        (ORDER_DELIVERED, "Order Delivered"),
        (ORDER_REJECTED, "Order Rejected"),
        (ORDER_COMPLETED, "Order Completed"),
    )
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=CART_STAGE)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    status = models.IntegerField(choices=ITEM_STATUS_CHOICES, default=LIVE)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return "Order - {} - {} ".format(self.id, self.owner)


class OrderedItem (models.Model):
    LIVE = 1
    DELETE = 0
    STATUS_CHOICES = (
        (LIVE, "Live"),
        (DELETE, "Delete"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="added_cart")
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="added_items")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

