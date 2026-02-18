import plotly.express as px
import pandas as pd
from database.db_engine import SessionLocal
from database.models import Customer


class ChartAgent:

    def generate_chart(self, query):

        print("\nCHART AGENT ACTIVE")
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

            query_lower = query.lower()

            if "churn" in query_lower:

                churn_by_persona = (
                    df.groupby("persona")["churn_risk"]
                    .mean()
                    .reset_index()
                )

                fig = px.bar(
                    churn_by_persona,
                    x="persona",
                    y="churn_risk"
                )

            else:

                fig = px.histogram(df, x="persona")

            return {
                "type": "chart",
                "data": fig.to_json()
            }

        finally:
            db.close()
