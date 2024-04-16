from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.models import Bar
from bar_app.serializers import BarSerializer

class BarListView(generics.ListAPIView):
    """
    Retrieve a list of all bars.
    """
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "name"]
    ordering_fields = ["id", "name"]

class BarCreateView(generics.CreateAPIView):
    """
    Create a new bar.
    """
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            serializer = self.get_serializer(data=request.data)
        elif isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Bar created successfully."},
            status=status.HTTP_201_CREATED
        )

class BarUpdateView(generics.UpdateAPIView):
    """
    Update an existing bar.
    """
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Bar updated successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

class BarDeleteView(generics.DestroyAPIView):
    """
    Delete an existing bar.
    """
    queryset = Bar.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Reference deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
