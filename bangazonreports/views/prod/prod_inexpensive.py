"""Report: Products where price < $1000"""
from django.shortcuts import render
from bangazonapi.models import Product

def inexpensive_product_list(request):

    if request.method == 'GET':

        prod_list = Product.objects.filter(price__lt=1000).values("name","price","description").order_by("price")

        template = 'prod/prod_inexpensive.html'
        context = {
            'inexpensive_product_list': prod_list
        }

        return render(request, template, context)