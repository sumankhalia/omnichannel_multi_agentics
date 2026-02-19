from core.llm.model_registry import get_client, get_model
import numpy as np

client = get_client()

VALID_CHARTS = {"bar", "line", "scatter", "pie", "heatmap"}


def select_chart(user_query, df):

    query_lower = user_query.lower()

    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(exclude=np.number).columns

    # ---------------------------------------------------
    # RULE-BASED INTELLIGENCE (PRIMARY — STABLE)
    # ---------------------------------------------------

    if df.empty:
        return "bar"

    # Trend / Time logic
    if "trend" in query_lower or "over time" in query_lower:
        if len(numeric_cols) >= 1:
            return "line"

    # Distribution logic
    if "distribution" in query_lower:
        return "bar"

    # Comparison logic
    if "by" in query_lower or "compare" in query_lower:
        if len(categorical_cols) >= 1:
            return "bar"

    # Relationship logic
    if len(numeric_cols) >= 2:
        if "correlation" in query_lower or "relationship" in query_lower:
            return "scatter"

    # Heatmap logic
    if len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
        if "heatmap" in query_lower:
            return "heatmap"

    # Pie logic
    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        if "share" in query_lower or "mix" in query_lower:
            return "pie"

    # ---------------------------------------------------
    # LLM FALLBACK (SECONDARY — FLEXIBLE)
    # ---------------------------------------------------

    try:

        prompt = f"""
You are a visualization intelligence agent.

Return ONLY ONE WORD:

bar
line
scatter
pie
heatmap

Business Question:
{user_query}

Dataset Columns:
{list(df.columns)}
"""

        response = client.chat.completions.create(
            model=get_model("chart_agent"),
            messages=[{"role": "user", "content": prompt}]
        )

        chart_type = response.choices[0].message.content.strip().lower()

        if chart_type not in VALID_CHARTS:
            chart_type = "bar"

        return chart_type

    except Exception:

        return "bar"
