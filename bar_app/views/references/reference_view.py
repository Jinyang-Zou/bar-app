from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from bar_app.serializers import ReferenceSerializer
from bar_app.models import Reference, Bar, Stock
import bar_app.utils.exceptions.api_exceptions as api_excs

class ListReferences(generics.ListAPIView):
    """
    A view for listing references.

    Only accessible to admin users.
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "name", "description"]
    ordering_fields = ["id", "name", "availability"]

    def get_queryset(self):
        """
        Get the queryset of references based on query parameters.

        Returns:
            queryset: Filtered queryset of references.
        """
        stocks = Stock.objects.all()
        references = Reference.objects.all()
        bar_id = self.request.query_params.get("bar_id")
        in_stock = self.request.query_params.get("in_stock")
        expected_params = ["bar_id", "in_stock"]
        params = self.request.query_params.keys()
        for param in params:
            if param not in expected_params:
                raise api_excs.UnknownParamException(
                    message=f"Unknown parameter: {param}.")

        if bar_id or in_stock:
            if bar_id:
                if not Bar.objects.filter(pk=bar_id).exists():
                    raise NotFound({"detail": "Invalid bar_id"})
                stocks = stocks.filter(bar=bar_id)
            if in_stock == "true":
                stocks = stocks.filter(stock__gt=0)
            elif in_stock == "false":
                stocks = stocks.filter(stock__exact=0)

            reference_ids = stocks.values_list("reference", flat=True)
            references = Reference.objects.filter(id__in=reference_ids)

        return references

    def get(self, request):
        """
        Get the list of references.

        Returns:
            Response: Response with the list of references.
        """
        references = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(references)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(references, many=True)
        return Response(serializer.data)

class CreateReference(generics.CreateAPIView):
    """
    A view for creating a reference.

    Only accessible to admin users.
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new reference.

        Returns:
            Response: Response indicating the success of the creation.
        """
        if isinstance(request.data, dict):
            serializer = self.get_serializer(data=request.data)
        elif isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "References created successfully."},
            status=status.HTTP_201_CREATED,
        )

class UpdateReference(generics.UpdateAPIView):
    """
    A view for updating a reference.

    Only accessible to admin users.
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Update an existing reference.

        Returns:
            Response: Response indicating the success of the update.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "References updated successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

class DeleteReference(generics.DestroyAPIView):
    """
    A view for deleting a reference.

    Only accessible to admin users.
    """
    queryset = Reference.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing reference.

        Returns:
            Response: Response indicating the success of the deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Reference deleted successfully"})
