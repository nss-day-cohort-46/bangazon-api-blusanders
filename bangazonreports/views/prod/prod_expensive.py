"""Report: Products where price >= $1000"""
from django.shortcuts import render
from bangazonapi.models import Product

def expensive_product_list(request):

    if request.method == 'GET':

        prod_list = Product.objects.filter(price__gt=999).values("name","price","description").order_by("price")

        template = 'prod/prod_expensive.html'
        context = {
            'expensive_product_list': prod_list
        }

        return render(request, template, context)