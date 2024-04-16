from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.serializers import StatisticsSerializer

class StatisticsView(generics.ListAPIView):
    """
    A view for retrieving statistics about stocks.

    Only accessible to admin users.
    """
    serializer_class = StatisticsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({
            "all_stocks": serializer.get_all_stocks(),
            "miss_at_least_one": serializer.get_miss_at_least_one()
        })