from django.urls import path
from bar_app.views import statistiques_view as stat_view

urlpatterns = [
    path("", stat_view.StatisticsView.as_view(), name="stat-list"),
]