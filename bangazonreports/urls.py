from django.urls import path
from .views import completed_orders_list
from .views import incomplete_orders_list
from .views import user_favorites_list

urlpatterns = [
    path('reports/orderscompleted', completed_orders_list),
    path('reports/ordersincomplete', incomplete_orders_list),
    path('reports/usersfav', user_favorites_list),
]