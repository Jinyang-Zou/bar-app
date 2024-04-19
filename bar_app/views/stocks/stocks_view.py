from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.models import Stock
from bar_app.serializers import StockSerializer

class StockListView(generics.ListAPIView):
    """
    A view for listing all stocks.

    Only accessible to admin users.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "reference_id", "bar_id", "stock"]
    ordering_fields = ["id", "reference_id", "bar_id", "stock"]
