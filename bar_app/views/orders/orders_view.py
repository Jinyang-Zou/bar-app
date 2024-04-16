from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.models import Order
from bar_app.serializers import OrderSerializer
from bar_app.utils.permissions import IsCustomer

class OrderListView(generics.ListAPIView):
    """
    A view for listing orders.

    Only accessible to admin users.
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "bar__name", "items__reference__name"]
    ordering_fields = ["id", "bar__name", "items__reference__name", "items__count"]


    def get(self, request, *args, **kwargs):
        orders = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(orders, many=True)
        page = self.paginate_queryset(orders)

        formatted_orders = []
        for order_data in serializer.data:
            formatted_order = {
                "id": order_data["id"],
                "bar": order_data["bar"],
            }
            if order_data.get("items"):
                formatted_order["items"] = order_data["items"]
            formatted_orders.append(formatted_order)

        return self.get_paginated_response(formatted_orders)


class OrderCreateView(generics.CreateAPIView):
    """
    A view for creating an order.

    Only accessible to authenticated customers.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        serializer.is_valid()
        order = serializer.save()
        return order
