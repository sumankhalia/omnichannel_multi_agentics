import pandas as pd
from database.db_engine import SessionLocal
from database.models import Transaction


class DataAgent:

    def analyze(self, query):

        print("\n🔥 DATA AGENT ACTIVE")
        print("Query:", query)

        db = SessionLocal()

        try:

            txns = db.query(Transaction).all()

            df = pd.DataFrame([
                {
                    "amount": t.amount,
                    "channel": t.channel,
                    "product": t.product_name
                }
                for t in txns
            ])

            total_revenue = df["amount"].sum()

            revenue_by_channel = (
                df.groupby("channel")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            top_channel = revenue_by_channel.index[0]

            return {
                "type": "analytics",
                "data": f"Total revenue: {total_revenue:.2f}. Top channel: {top_channel}"
            }

        finally:
            db.close()
