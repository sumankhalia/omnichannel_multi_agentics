from core.llm.model_registry import get_client, get_model
from analytics.query_engine import run_query
from core.agents.chart_agent import select_chart

client = get_client()

# =========================================================
# DATASET SUMMARIZER (TOKEN SAFE)
# =========================================================

def summarize_dataframe(df):

    if df is None or len(df) == 0:
        return "Empty dataset"

    summary = f"""
Rows: {len(df)}
Columns: {len(df.columns)}

Column Summary:
"""

    for col in df.columns:
        summary += f"- {col}\n"

    return summary


# Backward compatibility (VERY IMPORTANT)
def summarise_dataframe(df):
    return summarize_dataframe(df)


# =========================================================
# SQL GENERATION
# =========================================================

def generate_sql(user_query):

    sql_prompt = f"""
Convert this business question into SQL.

STRICT RULES:
- Database Type: SQLite
- Use SQLite-compatible syntax ONLY
- DO NOT use INTERVAL
- DO NOT use FILTER
- DO NOT use NOW()
- Use datetime() functions when needed

Tables:
customers(customer_id, signup_date, persona, churn_risk, preferred_channel, age)
transactions(transaction_id, customer_id, product_name, amount, channel, timestamp)
engagement_events(event_id, customer_id, event_type, channel, timestamp)

Question:
{user_query}

Return ONLY SQL.
"""

    response = client.chat.completions.create(
        model=get_model("sql_agent"),
        messages=[{"role": "user", "content": sql_prompt}]
    )

    return response.choices[0].message.content.strip()


# =========================================================
# RESULT INTERPRETATION
# =========================================================

def interpret_results(user_query, sql_query, df, market_context=None):

    dataset_summary = summarize_dataframe(df)

    interpretation_prompt = f"""
You are an Executive Business Intelligence AI.

STRICT RESPONSE RULES:

EXECUTIVE SUMMARY:
(max 3 lines)

KEY FINDINGS:
(max 5 bullets)

BUSINESS IMPLICATION:
(max 2 lines)

RECOMMENDED ACTIONS:
(max 3 bullets)

---

Business Question:
{user_query}

SQL Used:
{sql_query}

Dataset Summary:
{dataset_summary}

Market Context:
{market_context if market_context else "None"}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": interpretation_prompt}]
    )

    return response.choices[0].message.content


# =========================================================
# MASTER FLOW
# =========================================================

def ask_with_data(user_query, market_context=None):

    thinking_log = []

    thinking_log.append("Generating SQL...")

    sql_query = generate_sql(user_query)

    thinking_log.append(sql_query)

    result = run_query(sql_query)

    if isinstance(result, str):

        return {
            "insight": result,
            "chart": None,
            "data": None,
            "thinking": thinking_log
        }

    chart = select_chart(user_query, result)

    insight = interpret_results(user_query, sql_query, result, market_context)

    thinking_log.append("Insight generated.")

    return {
        "insight": insight,
        "chart": chart,
        "data": result,
        "thinking": thinking_log
    }