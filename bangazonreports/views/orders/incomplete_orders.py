"""Module for generating orders report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def incomplete_orders_list(request):

    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            #get all completed orders
            db_cursor.execute("""
                    SELECT
                        o.*,
                        u.first_name, u.last_name,
                        sum(p.price) as totalPrice
                    FROM
                        bangazonapi_order o
                    JOIN
                        bangazonapi_customer c ON o.customer_id = c.id
                    JOIN
                        bangazonapi_orderproduct op on op.order_id = o.id 
                    JOIN
                        bangazonapi_product p on op.product_id = p.id 
                    JOIN
                        auth_user u ON c.user_id = u.id

                    where payment_type_id is NULL

                    group by c.id
					order by o.id
                """)
            dataset = db_cursor.fetchall()

            incomplete_orders_list = []

            for row in dataset:
                incomplete_orders = {}
                incomplete_orders["id"] = row["id"]
                incomplete_orders["first_name"] = row["first_name"]
                incomplete_orders["last_name"] = row["last_name"]
                incomplete_orders["total_price"] = row["totalPrice"]

                # Add the current game to the `games` list for it
                incomplete_orders_list.append(incomplete_orders)

        template = 'orders/incomplete_orders.html'
        context = {
            'incomplete_orders_list': incomplete_orders_list
        }

        return render(request, template, context)