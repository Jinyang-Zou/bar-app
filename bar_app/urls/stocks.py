from django.urls import path
from bar_app.views import stocks_view

urlpatterns = [
    path("", stocks_view.StockListView.as_view(), name="stocks-list"),
]