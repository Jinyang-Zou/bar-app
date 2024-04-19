from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.models import Bar
from bar_app.serializers import BarSerializer

class BarViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Bar objects.
    """
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "name"]
    ordering_fields = ["id", "name"]
