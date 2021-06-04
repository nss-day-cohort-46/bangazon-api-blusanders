"""Module for generating orders report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection
from django.db.models import Sum

def completed_orders_list(request):

    if request.method == 'GET':

        completed_orders_list = Order.objects.filter(payment_type__isnull=False, lineitems__isnull=False).annotate(total_price=Sum('lineitems__product__price'))

        template = 'orders/completed_orders.html'
        context = {
            'completed_orders_list': completed_orders_list
        }

        return render(request, template, context)