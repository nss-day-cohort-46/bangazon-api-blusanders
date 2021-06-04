"""Module for generating user favorites report"""
from bangazonapi.models.favorite import Favorite
from bangazonapi.models.customer import Customer
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def user_favorites_list(request):

    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            #get all completed orders
            db_cursor.execute("""
                    SELECT
                    f.*,
                    u.last_name || ", " || u.first_name as cName,
                    s.last_name || ", " || s.first_name as sName

                    FROM bangazonapi_favorite f

                    JOIN bangazonapi_customer c on c.id = f.customer_id
                    JOIN auth_user u ON c.user_id = u.id
                    JOIN bangazonapi_customer cc on cc.id = f.seller_id
                    JOIN auth_user s ON cc.user_id = s.id
                    order by cName, sName
                """)
            dataset = db_cursor.fetchall()

            list_of_users_with_favorites = {}

            for row in dataset:
                fav = Customer()
                fav.sName = row["sName"]
                
                uid = row["customer_id"]

                if uid in list_of_users_with_favorites:

                    list_of_users_with_favorites[uid]['sellers'].append(fav)

                else:
                    list_of_users_with_favorites[uid] = {}
                    list_of_users_with_favorites[uid]["id"] = uid
                    list_of_users_with_favorites[uid]["cName"] = row["cName"]
                    list_of_users_with_favorites[uid]["sellers"] = [fav]

        list_of_favs = list_of_users_with_favorites.values()

        template = 'users/users_fav.html'
        context = {
            'user_favorites_list': list_of_favs
        }

        return render(request, template, context)