# Mock Paytm Merchant Data
import random
from datetime import datetime, timedelta

MERCHANT = {
    "name": "Rajesh Kirana Store",
    "merchant_id": "MID_7823412",
    "category": "Grocery",
    "location": "Delhi",
    "monthly_gmv": 145000,
    "paytm_balance": 12340,
}

INVENTORY = [
    {"item": "Basmati Rice (5kg)", "stock": 3, "daily_sales": 0.2, "price": 320, "days_in_stock": 45},
    {"item": "Tata Salt (1kg)", "stock": 52, "daily_sales": 4.1, "price": 22, "days_in_stock": 5},
    {"item": "Amul Butter (500g)", "stock": 8, "daily_sales": 3.2, "price": 275, "days_in_stock": 3},
    {"item": "Maggi Noodles (12pk)", "stock": 1, "daily_sales": 2.8, "price": 144, "days_in_stock": 60},
    {"item": "Colgate Toothpaste", "stock": 14, "daily_sales": 1.1, "price": 89, "days_in_stock": 10},
    {"item": "Parle-G Biscuits", "stock": 200, "daily_sales": 15.0, "price": 10, "days_in_stock": 2},
    {"item": "Aashirvaad Atta (10kg)", "stock": 2, "daily_sales": 0.3, "price": 450, "days_in_stock": 55},
]

PENDING_PAYMENTS = [
    {"customer": "Suresh Kumar", "phone": "+91-98101-11111", "amount": 850, "due_days": 12, "items": "Groceries"},
    {"customer": "Priya Sharma", "phone": "+91-98101-22222", "amount": 1200, "due_days": 7, "items": "Monthly ration"},
    {"customer": "Amit Verma", "phone": "+91-98101-33333", "amount": 420, "due_days": 3, "items": "Dairy + snacks"},
    {"customer": "Meena Devi", "phone": "+91-98101-44444", "amount": 290, "due_days": 21, "items": "Rice + dal"},
]

SALES_TREND = {
    "today": 4200,
    "yesterday": 3800,
    "this_week": 24500,
    "last_week": 21000,
    "best_selling_today": ["Parle-G Biscuits", "Tata Salt", "Amul Butter"],
    "slowest_this_week": ["Basmati Rice (5kg)", "Aashirvaad Atta (10kg)", "Maggi Noodles (12pk)"],
}

def get_merchant_context():
    return {
        "merchant": MERCHANT,
        "inventory": INVENTORY,
        "pending_payments": PENDING_PAYMENTS,
        "sales_trend": SALES_TREND,
    }
