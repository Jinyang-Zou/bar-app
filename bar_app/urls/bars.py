from django.urls import path
from bar_app.views import bar_view

urlpatterns = [
    path("", bar_view.BarListView.as_view(), name="bars-list"),
    path("create/", bar_view.BarCreateView.as_view(), name="create-bar"),
    path("update/<int:pk>", bar_view.BarUpdateView.as_view(), name="update-bar"),
    path("delete/<int:pk>", bar_view.BarDeleteView.as_view(), name="delete-bar"),
]