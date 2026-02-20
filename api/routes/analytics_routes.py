from fastapi import APIRouter
from pydantic import BaseModel
from analytics.query_engine import run_query

router = APIRouter()

class AnalyticsRequest(BaseModel):
    metric: str


# =========================================================
# METRIC REGISTRY  (THIS = YOUR DASHBOARD LOGIC)
# =========================================================

METRIC_REGISTRY = {

    # ---------------- REVENUE ----------------

    "revenue_trend": {
        "sql": """
            SELECT DATE(timestamp) as date, SUM(amount) as value
            FROM transactions
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """,
        "chart": "line"
    },

    "revenue_by_channel": {
        "sql": """
            SELECT channel as label, SUM(amount) as value
            FROM transactions
            GROUP BY channel
        """,
        "chart": "pie"
    },

    "revenue_distribution": {
        "sql": """
            SELECT amount
            FROM transactions
        """,
        "chart": "histogram"
    },

    "revenue_boxplot_by_channel": {
        "sql": """
            SELECT channel, amount
            FROM transactions
        """,
        "chart": "box"
    },

    # ---------------- PRODUCTS ----------------

    "top_products": {
        "sql": """
            SELECT product_name as label, SUM(amount) as value
            FROM transactions
            GROUP BY product_name
            ORDER BY value DESC
        """,
        "chart": "bar"
    },

    "product_channel_matrix": {
        "sql": """
            SELECT product_name, channel, SUM(amount) as value
            FROM transactions
            GROUP BY product_name, channel
        """,
        "chart": "heatmap"
    },

    # ---------------- CUSTOMERS ----------------

    "persona_distribution": {
        "sql": """
            SELECT persona as label, COUNT(*) as value
            FROM customers
            GROUP BY persona
        """,
        "chart": "bar"
    },

    "churn_risk_distribution": {
        "sql": """
            SELECT churn_risk
            FROM customers
        """,
        "chart": "histogram"
    },

    "age_vs_churn": {
        "sql": """
            SELECT age, churn_risk
            FROM customers
        """,
        "chart": "scatter"
    },

    "churn_heatmap": {
        "sql": """
            SELECT persona, preferred_channel, AVG(churn_risk) as value
            FROM customers
            GROUP BY persona, preferred_channel
        """,
        "chart": "heatmap"
    },

    # ---------------- ENGAGEMENT ----------------

    "event_frequency": {
        "sql": """
            SELECT event_type as label, COUNT(*) as value
            FROM engagement_events
            GROUP BY event_type
        """,
        "chart": "bar"
    },

    "engagement_trend": {
        "sql": """
            SELECT DATE(timestamp) as date, COUNT(*) as value
            FROM engagement_events
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """,
        "chart": "line"
    },

    "channel_mix": {
        "sql": """
            SELECT channel as label, COUNT(*) as value
            FROM engagement_events
            GROUP BY channel
        """,
        "chart": "pie"
    }
}


# =========================================================
# UNIVERSAL ANALYTICS ENDPOINT
# =========================================================

@router.post("/analytics/query")
def run_analytics(req: AnalyticsRequest):

    if req.metric not in METRIC_REGISTRY:
        return {"error": f"Unknown metric: {req.metric}"}

    config = METRIC_REGISTRY[req.metric]

    df = run_query(config["sql"])

    if isinstance(df, str):
        return {"error": df}

    return {
        "metric": req.metric,
        "chart": config["chart"],
        "data": df.to_dict(orient="records")
    }