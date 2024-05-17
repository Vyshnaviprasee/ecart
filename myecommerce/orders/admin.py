from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_status', 'status', 'owner')
    list_filter = (
        'owner', 
        'status',
        'order_status',
        )
    search_fields = ('id', 'owner', 'status', 'order_status')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)


