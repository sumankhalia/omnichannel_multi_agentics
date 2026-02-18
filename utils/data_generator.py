import random
import numpy as np
from faker import Faker
from database.db_engine import SessionLocal
from database.models import Customer, Transaction, EngagementEvent

fake = Faker()
np.random.seed(42)

PERSONAS = ["VIP", "Loyal", "Discount Hunter", "Impulse Buyer", "Churn Risk"]

PRODUCTS = [
    "Wireless Earbuds",
    "Running Shoes",
    "Vitamin C Serum",
    "Protein Bars",
    "Smart Watch",
    "Bluetooth Speaker"
]


# ---------------------------------------------------
# REALISTIC CHURN MODEL
# ---------------------------------------------------

def generate_churn_risk(persona):

    churn_profile = {
        "VIP": random.uniform(0.05, 0.20),
        "Loyal": random.uniform(0.10, 0.35),
        "Impulse Buyer": random.uniform(0.25, 0.55),
        "Discount Hunter": random.uniform(0.35, 0.70),
        "Churn Risk": random.uniform(0.65, 0.95)
    }

    return round(churn_profile.get(persona, random.uniform(0.2, 0.6)), 2)


# ---------------------------------------------------
# TRANSACTION LOGIC (Persona Driven)
# ---------------------------------------------------

def transaction_count(persona):

    profile = {
        "VIP": random.randint(8, 20),
        "Loyal": random.randint(5, 15),
        "Impulse Buyer": random.randint(3, 12),
        "Discount Hunter": random.randint(2, 10),
        "Churn Risk": random.randint(1, 6)
    }

    return profile.get(persona, random.randint(1, 10))


def transaction_amount(persona):

    profile = {
        "VIP": random.uniform(300, 1500),
        "Loyal": random.uniform(150, 900),
        "Impulse Buyer": random.uniform(80, 600),
        "Discount Hunter": random.uniform(40, 350),
        "Churn Risk": random.uniform(20, 200)
    }

    return round(profile.get(persona, random.uniform(50, 500)), 2)


# ---------------------------------------------------
# ENGAGEMENT LOGIC (Persona Driven)
# ---------------------------------------------------

def engagement_volume(persona):

    profile = {
        "VIP": random.randint(20, 80),
        "Loyal": random.randint(25, 90),
        "Impulse Buyer": random.randint(15, 70),
        "Discount Hunter": random.randint(10, 60),
        "Churn Risk": random.randint(5, 25)
    }

    return profile.get(persona, random.randint(10, 50))


EVENT_TYPES = [
    "page_view",
    "search",
    "add_to_cart",
    "wishlist_add",
    "email_open",
    "push_click",
    "purchase_intent"
]


# ---------------------------------------------------
# MAIN GENERATOR
# ---------------------------------------------------

def generate_data():

    db = SessionLocal()

    print("Generating Relational Customer Ecosystem...\n")

    for i in range(5000):

        persona = random.choice(PERSONAS)

        churn_risk = generate_churn_risk(persona)

        customer = Customer(
            customer_id=i + 1,
            name=fake.name(),
            age=random.randint(18, 65),
            city=fake.city(),
            persona=persona,
            preferred_channel=random.choice(["Email", "Push", "SMS"]),
            churn_risk=churn_risk 
        )

        db.add(customer)

        # -----------------------------
        # Transactions → RELATIONAL
        # -----------------------------
        for t in range(transaction_count(persona)):

            txn = Transaction(
                customer_id=i + 1,
                product_name=random.choice(PRODUCTS),
                amount=transaction_amount(persona),
                channel=random.choice(["Online", "Store", "App"])
            )

            db.add(txn)

        # -----------------------------
        # Events → RELATIONAL
        # -----------------------------
        for e in range(engagement_volume(persona)):

            event = EngagementEvent(
                customer_id=i + 1,
                event_type=random.choice(EVENT_TYPES),
                channel=random.choice(["App", "Web", "Email"])
            )

            db.add(event)

    db.commit()
    db.close()

    print("\nRelational Ecosystem Generated Successfully")


# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------

if __name__ == "__main__":
    generate_data()
