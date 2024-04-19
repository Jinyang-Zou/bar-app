from django.urls import path
from bar_app.views import orders_view

urlpatterns = [
    path("", orders_view.OrderListView.as_view(), name="orders-list"),
    path("create/", orders_view.OrderCreateView.as_view(), name="create-order"),
]
