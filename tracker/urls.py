from django.urls import path
from django.views.generic import RedirectView

from .views import (
    CategoryExpenseAPIView,
    DashboardView,
    ExpenseTrendAPIView,
    MonthlySummaryAPIView,
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("api/monthly-summary/", MonthlySummaryAPIView.as_view(), name="api-monthly-summary"),
    path("api/category-expense/", CategoryExpenseAPIView.as_view(), name="api-category-expense"),
    path("api/expense-trend/", ExpenseTrendAPIView.as_view(), name="api-expense-trend"),
]
