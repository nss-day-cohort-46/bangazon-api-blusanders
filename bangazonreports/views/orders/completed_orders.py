"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order

def completed_orders_list(request):

    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            #get all completed orders
            db_cursor.execute("""
                SELECT
                    o.*,
                    u.first_name, u.last_name
                FROM
                    bangazonapi_order o
                JOIN
                    bangazonapi_customer c ON o.customer_id = c.id
                JOIN
                    auth_user u ON c.user_id = u.id

                where payment_type_id is not NULL
                order by created_date
                """)
            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "maker": "Bar Games",
            #                 "skill_level": 3,
            #                 "number_of_players": 4,
            #                 "gametype_id": 2
            #             }
            #         ]
            #     }
            # }

            completed_orders = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                order = Order()
                game.title = row["title"]
                game.maker = row["maker"]
                game.skill_level = row["skill_level"]
                game.number_of_players = row["number_of_players"]
                game.gametype_id = row["gametype_id"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in games_by_user:

                    # Add the current game to the `games` list for it
                    games_by_user[uid]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_games = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)