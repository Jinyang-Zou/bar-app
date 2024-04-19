from django.urls import path
from bar_app.views import reference_view

urlpatterns = [
    path("", reference_view.ListReferences.as_view(), name="reference-list"),
    path("create/", reference_view.CreateReference.as_view(), name="create-reference"),
    path("update/<int:pk>", reference_view.UpdateReference.as_view(), name="update-reference"),
    path("delete/<int:pk>", reference_view.DeleteReference.as_view(), name="delete-reference"),
]