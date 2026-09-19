# Paytm Merchant Data Store (Dynamic + Customizable + Demo Profiles)
import json
import os

# Default demo profiles for hackathon presentation
PRESET_PROFILES = {
    "custom": {
        "merchant": {
            "name": "My Business Store",
            "merchant_id": "MID_LIVE_998811",
            "category": "Retail & Services",
            "location": "Bengaluru",
            "monthly_gmv": 210000,
            "paytm_balance": 18450,
            "upi_id": "merchant@paytm",
            "phone": "+91-98765-43210"
        },
        "inventory": [
            {"item": "Fast-Moving Goods", "stock": 45, "daily_sales": 5.0, "price": 199, "days_in_stock": 4},
            {"item": "Premium Accessory Kit", "stock": 2, "daily_sales": 1.2, "price": 899, "days_in_stock": 42},
            {"item": "Daily Essentials Pack", "stock": 80, "daily_sales": 8.5, "price": 99, "days_in_stock": 2},
            {"item": "Slow Moving Clearance Item", "stock": 15, "daily_sales": 0.1, "price": 549, "days_in_stock": 65},
            {"item": "Top Selling Combo", "stock": 3, "daily_sales": 2.5, "price": 350, "days_in_stock": 5}
        ],
        "pending_payments": [
            {"customer": "Rahul Verma", "phone": "+91-98101-55555", "amount": 1450, "due_days": 14, "items": "Bulk order"},
            {"customer": "Ananya Sen", "phone": "+91-98101-66666", "amount": 820, "due_days": 9, "items": "Monthly supplies"},
            {"customer": "Vikram Malhotra", "phone": "+91-98101-77777", "amount": 3200, "due_days": 21, "items": "Custom order balance"}
        ],
        "sales_trend": {
            "today": 6800,
            "yesterday": 5200,
            "this_week": 41200,
            "last_week": 34500,
            "best_selling_today": ["Daily Essentials Pack", "Fast-Moving Goods"],
            "slowest_this_week": ["Slow Moving Clearance Item", "Premium Accessory Kit"]
        }
    },
    "electronics": {
        "merchant": {
            "name": "Apex Tech & Mobile Hub",
            "merchant_id": "MID_TECH_44120",
            "category": "Consumer Electronics",
            "location": "Mumbai",
            "monthly_gmv": 480000,
            "paytm_balance": 42300,
            "upi_id": "apextech@paytm",
            "phone": "+91-98200-11223"
        },
        "inventory": [
            {"item": "Fast Charging Cable (Type-C)", "stock": 60, "daily_sales": 6.2, "price": 299, "days_in_stock": 3},
            {"item": "Wireless Earbuds Gen2", "stock": 2, "daily_sales": 1.4, "price": 1499, "days_in_stock": 15},
            {"item": "10000mAh Power Bank", "stock": 1, "daily_sales": 0.9, "price": 999, "days_in_stock": 35},
            {"item": "Tempered Glass Screen Protector", "stock": 120, "daily_sales": 12.0, "price": 150, "days_in_stock": 2},
            {"item": "Bluetooth Speaker (Old Gen)", "stock": 9, "daily_sales": 0.1, "price": 1200, "days_in_stock": 70}
        ],
        "pending_payments": [
            {"customer": "Sameer Joshi", "phone": "+91-98201-99887", "amount": 2500, "due_days": 18, "items": "Earbuds + Charger repair"},
            {"customer": "Neha Kapoor", "phone": "+91-98201-44332", "amount": 1200, "due_days": 8, "items": "Accessories bill"}
        ],
        "sales_trend": {
            "today": 12400,
            "yesterday": 9800,
            "this_week": 82000,
            "last_week": 69000,
            "best_selling_today": ["Fast Charging Cable (Type-C)", "Tempered Glass Screen Protector"],
            "slowest_this_week": ["Bluetooth Speaker (Old Gen)", "10000mAh Power Bank"]
        }
    },
    "cafe": {
        "merchant": {
            "name": "Bean & Brew Cafe",
            "merchant_id": "MID_CAFE_88712",
            "category": "Food & Beverage",
            "location": "Delhi NCR",
            "monthly_gmv": 195000,
            "paytm_balance": 15600,
            "upi_id": "beanbrew@paytm",
            "phone": "+91-98111-22334"
        },
        "inventory": [
            {"item": "Artisan Coffee Beans (1kg)", "stock": 2, "daily_sales": 0.8, "price": 650, "days_in_stock": 28},
            {"item": "Milk Cartons (Pack of 12)", "stock": 3, "daily_sales": 2.5, "price": 720, "days_in_stock": 2},
            {"item": "Croissants (Frozen batch)", "stock": 24, "daily_sales": 6.0, "price": 85, "days_in_stock": 1},
            {"item": "Caramel Syrup (750ml)", "stock": 1, "daily_sales": 0.3, "price": 450, "days_in_stock": 45},
            {"item": "Paper Cups & Sleeves (500pk)", "stock": 450, "daily_sales": 35.0, "price": 4, "days_in_stock": 5}
        ],
        "pending_payments": [
            {"customer": "Office Catering (Innovate Corp)", "phone": "+91-98112-99001", "amount": 4800, "due_days": 15, "items": "Corporate coffee buffet"},
            {"customer": "Kunal Singhal", "phone": "+91-98112-55443", "amount": 650, "due_days": 6, "items": "Weekly tab"}
        ],
        "sales_trend": {
            "today": 5800,
            "yesterday": 4900,
            "this_week": 36500,
            "last_week": 31000,
            "best_selling_today": ["Croissants", "Paper Cups & Sleeves"],
            "slowest_this_week": ["Caramel Syrup", "Artisan Coffee Beans"]
        }
    }
}

# Active in-memory state that can be updated dynamically by user
ACTIVE_MERCHANT = dict(PRESET_PROFILES["custom"]["merchant"])
ACTIVE_INVENTORY = list(PRESET_PROFILES["custom"]["inventory"])
ACTIVE_PENDING_PAYMENTS = list(PRESET_PROFILES["custom"]["pending_payments"])
ACTIVE_SALES_TREND = dict(PRESET_PROFILES["custom"]["sales_trend"])

def load_profile(profile_key: str):
    """Load a demo or custom profile."""
    global ACTIVE_MERCHANT, ACTIVE_INVENTORY, ACTIVE_PENDING_PAYMENTS, ACTIVE_SALES_TREND
    if profile_key in PRESET_PROFILES:
        ACTIVE_MERCHANT = dict(PRESET_PROFILES[profile_key]["merchant"])
        ACTIVE_INVENTORY = list(PRESET_PROFILES[profile_key]["inventory"])
        ACTIVE_PENDING_PAYMENTS = list(PRESET_PROFILES[profile_key]["pending_payments"])
        ACTIVE_SALES_TREND = dict(PRESET_PROFILES[profile_key]["sales_trend"])

def update_merchant_info(name=None, merchant_id=None, category=None, location=None, balance=None, upi_id=None, phone=None):
    """Allows user to customize their own merchant store details in real-time."""
    global ACTIVE_MERCHANT
    if name is not None: ACTIVE_MERCHANT["name"] = name
    if merchant_id is not None: ACTIVE_MERCHANT["merchant_id"] = merchant_id
    if category is not None: ACTIVE_MERCHANT["category"] = category
    if location is not None: ACTIVE_MERCHANT["location"] = location
    if balance is not None: ACTIVE_MERCHANT["paytm_balance"] = balance
    if upi_id is not None: ACTIVE_MERCHANT["upi_id"] = upi_id
    if phone is not None: ACTIVE_MERCHANT["phone"] = phone

def add_pending_payment(customer: str, phone: str, amount: float, due_days: int, items: str):
    """Add a real or test customer debt to track in real-time."""
    global ACTIVE_PENDING_PAYMENTS
    ACTIVE_PENDING_PAYMENTS.append({
        "customer": customer,
        "phone": phone,
        "amount": amount,
        "due_days": due_days,
        "items": items
    })

def add_inventory_item(item: str, stock: int, daily_sales: float, price: float, days_in_stock: int):
    """Add a custom product to the live inventory."""
    global ACTIVE_INVENTORY
    ACTIVE_INVENTORY.append({
        "item": item,
        "stock": stock,
        "daily_sales": daily_sales,
        "price": price,
        "days_in_stock": days_in_stock
    })

def get_merchant_context():
    """Returns live context for the AI agent tools."""
    return {
        "merchant": ACTIVE_MERCHANT,
        "inventory": ACTIVE_INVENTORY,
        "pending_payments": ACTIVE_PENDING_PAYMENTS,
        "sales_trend": ACTIVE_SALES_TREND,
    }

# Backward compatibility references
MERCHANT = ACTIVE_MERCHANT
INVENTORY = ACTIVE_INVENTORY
PENDING_PAYMENTS = ACTIVE_PENDING_PAYMENTS
SALES_TREND = ACTIVE_SALES_TREND

