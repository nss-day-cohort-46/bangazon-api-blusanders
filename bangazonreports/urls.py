from django.urls import path
from .views import orders_completed_list

urlpatterns = [
    path('reports/orderscompleted', orders_completed_list),
]