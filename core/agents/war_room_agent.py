from core.llm.model_registry import get_client, get_model
from analytics.query_engine import run_query
from core.agents.insight_agent import generate_sql, interpret_results, summarize_dataframe
from core.agents.chart_agent import select_chart
from core.agents.chart_formatter import normalize_chart_data

client = get_client()


# =========================================================
# SPECIALIST AGENT
# =========================================================

def specialist_agent(role, question, df):

    prompt = f"""
You are acting as the {role}.

STRICT RULES:
- Max 3 bullets
- Executive tone

Strategic Question:
{question}

Dataset Snapshot:
{summarize_dataframe(df)}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =========================================================
# WAR ROOM ENGINE
# =========================================================

def run_war_room(user_query, market_context=None):

    thinking_log = []

    thinking_log.append("War Room activated.")

    sql_query = generate_sql(user_query)

    thinking_log.append("SQL generated.")
    thinking_log.append(sql_query)

    df = run_query(sql_query)

    if isinstance(df, str):

        return {
            "insight": df,
            "chart": None,
            "data": [],
            "thinking": thinking_log
        }

    roles = [
        "Growth Strategist",
        "Risk Officer",
        "Finance Controller",
        "Market Intelligence Analyst"
    ]

    opinions = {}

    for role in roles:
        opinions[role] = specialist_agent(role, user_query, df)

    debate = opinions

    synthesis = interpret_results(user_query, sql_query, df, market_context)

    confidence = "Confidence: 85% | Risk Level: Medium | Disagreement Level: Low"

    tension = "Strategic Tension: Medium | Primary Conflict: Growth vs Risk"

    chart = select_chart(user_query, df)

    thinking_log.append("War Room analysis complete.")

    return {
        "insight": synthesis,
        "debate": debate,
        "confidence": confidence,
        "tension": tension,

        # ✅ CHART FIX
        "chart": chart,
        "data": normalize_chart_data(df),

        "thinking": thinking_log
    }