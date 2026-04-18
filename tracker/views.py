from calendar import month_name
from datetime import date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic import TemplateView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Expense, Income


def _month_year_from_request(request):
    today = timezone.localdate()
    try:
        month = int(request.GET.get("month", today.month))
        year = int(request.GET.get("year", today.year))
    except (TypeError, ValueError):
        month, year = today.month, today.year

    if month < 1 or month > 12:
        month = today.month

    return month, year


def _month_range(year: int, month: int):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return start, end


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tracker/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["selected_month"] = today.month
        context["selected_year"] = today.year
        context["months"] = [{"value": i, "label": month_name[i]} for i in range(1, 13)]
        return context


class MonthlySummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month, year = _month_year_from_request(request)
        start_date, end_date = _month_range(year, month)

        incomes = Income.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date)
        expenses = Expense.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date)

        total_income = incomes.aggregate(total=Sum("amount")).get("total") or Decimal("0")
        total_expense = expenses.aggregate(total=Sum("amount")).get("total") or Decimal("0")

        return Response({
            "labels": ["Income", "Expenses"],
            "data": [float(total_income), float(total_expense)],
        })


class CategoryExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month, year = _month_year_from_request(request)
        start_date, end_date = _month_range(year, month)

        category_totals = (
            Expense.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date)
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        labels = [entry["category__name"] for entry in category_totals]
        data = [float(entry["total"]) for entry in category_totals]

        return Response({"labels": labels, "data": data})


class ExpenseTrendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month, year = _month_year_from_request(request)
        _, end_date = _month_range(year, month)

        start_anchor = date(year, month, 1)
        start_month = start_anchor.month - 5
        start_year = start_anchor.year

        while start_month <= 0:
            start_month += 12
            start_year -= 1

        start_date = date(start_year, start_month, 1)

        rows = (
            Expense.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date)
            .annotate(period=TruncMonth("date"))
            .values("period")
            .annotate(total=Sum("amount"))
            .order_by("period")
        )

        labels = [row["period"].strftime("%b %Y") for row in rows if row["period"]]
        data = [float(row["total"]) for row in rows]

        return Response({"labels": labels, "data": data})