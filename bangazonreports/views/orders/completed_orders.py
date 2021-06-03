"""Module for generating orders report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def completed_orders_list(request):

    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            #get all completed orders
            db_cursor.execute("""
                    SELECT
                        o.*,
                        u.first_name, u.last_name,
                        py.merchant_name,
                        sum(p.price) as totalPrice
                    FROM bangazonapi_order o
                    JOIN bangazonapi_customer c ON o.customer_id = c.id
                    JOIN bangazonapi_orderproduct op on op.order_id = o.id 
                    JOIN bangazonapi_product p on op.product_id = p.id 
                    JOIN bangazonapi_payment py on py.id = o.payment_type_id
                    JOIN auth_user u ON c.user_id = u.id

                    where payment_type_id is not NULL
                    group by c.id
                """)
            dataset = db_cursor.fetchall()

            completed_orders_list = []

            for row in dataset:
                completed_orders = {}
                completed_orders["id"] = row["id"]
                completed_orders["first_name"] = row["first_name"]
                completed_orders["last_name"] = row["last_name"]
                completed_orders["merchant_name"] = row["merchant_name"]
                completed_orders["total_price"] = row["totalPrice"]

                completed_orders_list.append(completed_orders)

        template = 'orders/completed_orders.html'
        context = {
            'completed_orders_list': completed_orders_list
        }

        return render(request, template, context)