import random
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

from database.db_engine import SessionLocal
from database.models import Customer, Transaction, EngagementEvent

fake = Faker()
np.random.seed(42)

# ---------------------------------------------------
# BUSINESS CONFIG
# ---------------------------------------------------

CUSTOMER_COUNT = 5000

PERSONAS = [
    "VIP",
    "Loyal",
    "Discount Hunter",
    "Impulse Buyer",
    "Churn Risk",
    "High Potential",
    "Window Shopper",
    "Brand Advocate"
]

PRODUCTS = [
    "Wireless Earbuds",
    "Running Shoes",
    "Vitamin C Serum",
    "Protein Bars",
    "Smart Watch",
    "Bluetooth Speaker",
    "Gaming Mouse",
    "Mechanical Keyboard",
    "Fitness Band",
    "Organic Face Wash",
    "Laptop Stand",
    "Noise Cancelling Headphones"
]

EVENT_TYPES = [
    "page_view",
    "search",
    "add_to_cart",
    "wishlist_add",
    "email_open",
    "push_click",
    "purchase_intent",
    "product_compare",
    "review_read",
    "coupon_view",
    "checkout_abandon",
    "ad_click",
    "recommendation_click"
]

CHANNELS_TXN = ["Online", "Store", "App"]
CHANNELS_EVENT = ["App", "Web", "Email"]

START_DATE = datetime.now() - timedelta(days=180)
END_DATE = datetime.now()

# ---------------------------------------------------
# TIME ENGINE
# ---------------------------------------------------

def random_timestamp(start=START_DATE, end=END_DATE):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def channel_hour_bias(channel):

    if channel == "App":
        return int(np.clip(np.random.normal(20, 3), 0, 23))

    if channel == "Store":
        return int(np.clip(np.random.normal(14, 2), 0, 23))

    return int(np.clip(np.random.normal(11, 3), 0, 23))


# ---------------------------------------------------
# CHURN MODEL
# ---------------------------------------------------

def generate_churn_risk(persona):

    churn_profile = {
        "VIP": random.uniform(0.05, 0.20),
        "Loyal": random.uniform(0.10, 0.35),
        "Impulse Buyer": random.uniform(0.25, 0.55),
        "Discount Hunter": random.uniform(0.35, 0.70),
        "Churn Risk": random.uniform(0.65, 0.95),
        "High Potential": random.uniform(0.20, 0.45),
        "Window Shopper": random.uniform(0.40, 0.75),
        "Brand Advocate": random.uniform(0.05, 0.25)
    }

    return round(churn_profile.get(persona, random.uniform(0.2, 0.6)), 2)


# ---------------------------------------------------
# PERSONA BEHAVIOR MODELS
# ---------------------------------------------------

def transaction_count(persona):

    profile = {
        "VIP": random.randint(10, 25),
        "Loyal": random.randint(6, 18),
        "Impulse Buyer": random.randint(4, 14),
        "Discount Hunter": random.randint(3, 12),
        "Churn Risk": random.randint(1, 7),
        "High Potential": random.randint(5, 16),
        "Window Shopper": random.randint(1, 5),
        "Brand Advocate": random.randint(8, 22)
    }

    return profile.get(persona, random.randint(1, 10))


def transaction_amount(persona):

    profile = {
        "VIP": np.random.lognormal(mean=6.2, sigma=0.5),
        "Loyal": np.random.lognormal(mean=5.8, sigma=0.6),
        "Impulse Buyer": np.random.lognormal(mean=5.4, sigma=0.7),
        "Discount Hunter": np.random.lognormal(mean=5.0, sigma=0.8),
        "Churn Risk": np.random.lognormal(mean=4.6, sigma=0.9),
        "High Potential": np.random.lognormal(mean=5.6, sigma=0.7),
        "Window Shopper": np.random.lognormal(mean=4.8, sigma=0.8),
        "Brand Advocate": np.random.lognormal(mean=6.0, sigma=0.6)
    }

    return round(profile.get(persona, np.random.lognormal(5.3, 0.7)), 2)


def engagement_volume(persona):

    profile = {
        "VIP": random.randint(40, 120),
        "Loyal": random.randint(50, 140),
        "Impulse Buyer": random.randint(25, 90),
        "Discount Hunter": random.randint(20, 80),
        "Churn Risk": random.randint(8, 30),
        "High Potential": random.randint(35, 100),
        "Window Shopper": random.randint(15, 50),
        "Brand Advocate": random.randint(60, 160)
    }

    return profile.get(persona, random.randint(10, 60))


# ---------------------------------------------------
# ACTIVITY TIMELINE ENGINE (KEY REALISM)
# ---------------------------------------------------

def generate_activity_time(signup_date):

    """Ensures activity AFTER signup"""
    return random_timestamp(signup_date, END_DATE)


# ---------------------------------------------------
# MAIN GENERATOR
# ---------------------------------------------------

def generate_data():

    db = SessionLocal()

    print("Generating Business-Realistic Customer Ecosystem...\n")

    for i in range(CUSTOMER_COUNT):

        persona = random.choice(PERSONAS)

        churn_risk = generate_churn_risk(persona)
        signup_date = random_timestamp()

        customer = Customer(
            customer_id=i + 1,
            name=fake.name(),
            age=random.randint(18, 65),
            city=fake.city(),
            persona=persona,
            preferred_channel=random.choice(["Email", "Push", "SMS"]),
            churn_risk=churn_risk,
            signup_date=signup_date
        )

        db.add(customer)

        # -----------------------------
        # Transactions → AFTER SIGNUP
        # -----------------------------
        for _ in range(transaction_count(persona)):

            txn_time = generate_activity_time(signup_date)
            channel = random.choice(CHANNELS_TXN)

            txn_time = txn_time.replace(hour=channel_hour_bias(channel))

            txn = Transaction(
                customer_id=i + 1,
                product_name=random.choice(PRODUCTS),
                amount=transaction_amount(persona),
                channel=channel,
                timestamp=txn_time
            )

            db.add(txn)

        # -----------------------------
        # Events → AFTER SIGNUP
        # -----------------------------
        for _ in range(engagement_volume(persona)):

            event_time = generate_activity_time(signup_date)
            channel = random.choice(CHANNELS_EVENT)

            event_time = event_time.replace(hour=channel_hour_bias(channel))

            event = EngagementEvent(
                customer_id=i + 1,
                event_type=random.choice(EVENT_TYPES),
                channel=channel,
                timestamp=event_time
            )

            db.add(event)

    db.commit()
    db.close()

    print("\nBusiness-Realistic Ecosystem Generated Successfully")


# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------

if __name__ == "__main__":
    generate_data()
