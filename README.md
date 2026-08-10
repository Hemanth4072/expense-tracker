# Monthly Expense Tracker (Django + Chart.js Dashboard)

A Django-based expense tracker with a professional analytics dashboard powered by Chart.js.

## API Endpoints
- `GET /api/monthly-summary/?month=4&year=2026`
- `GET /api/category-expense/?month=4&year=2026`
- `GET /api/expense-trend/?month=4&year=2026`

### Example responses

`/api/monthly-summary/`
```json
{
  "labels": ["Income", "Expenses"],
  "data": [8200.0, 5475.5],
  "meta": {
    "month": 4,
    "year": 2026,
    "expense_change_vs_previous_month_pct": -7.34
  }
}
```

`/api/category-expense/`
```json
{
  "labels": ["Food", "Rent", "Transport"],
  "data": [1600.0, 2500.0, 450.0],
  "insights": [
    {"category": "Food", "amount": 1600.0, "percent": 29.22},
    {"category": "Rent", "amount": 2500.0, "percent": 45.66},
    {"category": "Transport", "amount": 450.0, "percent": 8.22}
  ]
}
```

`/api/expense-trend/`
```json
{
  "labels": ["Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026"],
  "data": [4200.0, 4400.0, 4700.0, 5100.0, 4950.0, 5475.5]
}
```

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/dashboard/` (login required).

