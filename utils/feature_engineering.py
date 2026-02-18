import pandas as pd
from database.db_engine import SessionLocal
from database.models import Customer, Transaction, EngagementEvent


class FeatureEngineering:

    def build_customer_features(self):

        db = SessionLocal()

        customers = db.query(Customer).all()
        transactions = db.query(Transaction).all()
        events = db.query(EngagementEvent).all()

        db.close()

        customers_df = pd.DataFrame([c.__dict__ for c in customers])
        transactions_df = pd.DataFrame([t.__dict__ for t in transactions])
        events_df = pd.DataFrame([e.__dict__ for e in events])

        # -----------------------------
        # TRANSACTION FEATURES
        # -----------------------------
        txn_features = transactions_df.groupby("customer_id").agg(
            total_spend=("amount", "sum"),
            purchase_count=("transaction_id", "count")
        ).reset_index()

        # -----------------------------
        # ENGAGEMENT FEATURES
        # -----------------------------
        event_features = events_df.groupby("customer_id").agg(
            event_count=("event_id", "count")
        ).reset_index()

        # -----------------------------
        # MERGE FEATURES
        # -----------------------------
        features_df = customers_df.merge(txn_features, on="customer_id", how="left")
        features_df = features_df.merge(event_features, on="customer_id", how="left")

        features_df.fillna(0, inplace=True)

        return features_df
