from django.contrib import admin

from .models import Category, Expense, Income


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "date", "note")
    list_filter = ("date",)
    search_fields = ("user__username", "note")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "date", "note")
    list_filter = ("category", "date")
    search_fields = ("user__username", "category__name", "note")
