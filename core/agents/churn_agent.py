import pandas as pd
from database.db_engine import SessionLocal
from database.models import Customer


class ChurnAgent:

    def analyze(self, query):

        print("\nCHURN AGENT ACTIVE")
        print("Query:", query)

        db = SessionLocal()

        try:

            customers = db.query(Customer).all()

            data = [
                {
                    "persona": c.persona,
                    "churn_risk": getattr(c, "churn_risk", 0.0)
                }
                for c in customers
            ]

            df = pd.DataFrame(data)

            avg_churn = df["churn_risk"].mean()

            churn_by_persona = (
                df.groupby("persona")["churn_risk"]
                .mean()
                .sort_values(ascending=False)
            )

            top_risk_persona = churn_by_persona.index[0]

            return {
                "type": "analytics",
                "data": f"Avg churn risk: {avg_churn:.2f}. Highest risk persona: {top_risk_persona}"
            }

        finally:
            db.close()
