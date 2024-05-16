from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    featured_products = Product.objects.order_by('-priority')[:4]
    latest_products = Product.objects.order_by('-id')[:4]
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products
    }
    return render(request, 'index.html', context)

def list_products(request):
    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    product_list = Product.objects.order_by('-priority').all()
    product_paginator = Paginator(product_list, 3)
    product_list = product_paginator.page(page)
    context = {
        'product_list': product_list
    }
    return render(request, 'product.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product

    }
    return render(request, 'product_detail.html', context)


