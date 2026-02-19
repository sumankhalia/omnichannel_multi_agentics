from core.llm.model_registry import get_client, get_model
from analytics.query_engine import run_query
from core.agents.chart_agent import select_chart

client = get_client()

# ---------------------------------------------------
# SQL GENERATION (SQLITE SAFE)
# ---------------------------------------------------

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


# ---------------------------------------------------
# EXECUTIVE INSIGHT INTERPRETATION
# ---------------------------------------------------

def interpret_results(user_query, sql_query, df, market_context=None):

    interpretation_prompt = f"""
You are an Executive Business Intelligence AI.

STRICT RESPONSE RULES:

- Be concise
- No storytelling
- No technical explanations
- Dashboard-ready language

MANDATORY FORMAT:

EXECUTIVE SUMMARY:
(max 3 lines)

KEY FINDINGS:
(max 5 bullets)

BUSINESS IMPLICATION:
(max 2 lines)

RECOMMENDED ACTIONS:
(max 3 bullets)

OPTIONAL VISUALIZATION:
(Suggest chart ONLY if useful)

---

Business Question:
{user_query}

SQL Used:
{sql_query}

Data Result:
{df.to_string()}

Market Context:
{market_context if market_context else "None"}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": interpretation_prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# MASTER SINGLE-AGENT FLOW
# ---------------------------------------------------

def ask_with_data(user_query, market_context=None):

    thinking_log = []

    thinking_log.append("Understanding business question...")

    sql_query = generate_sql(user_query)

    thinking_log.append("SQL generated:")
    thinking_log.append(sql_query)

    result = run_query(sql_query)

    if isinstance(result, str) and result.startswith("SQL_ERROR"):

        thinking_log.append("SQL failed. Attempting repair...")

        repair_prompt = f"""
The following SQLite query failed.

Error:
{result}

Original Query:
{sql_query}

Rewrite using STRICT SQLite syntax ONLY.

Return ONLY corrected SQL.
"""

        repair_response = client.chat.completions.create(
            model=get_model("sql_agent"),
            messages=[{"role": "user", "content": repair_prompt}]
        )

        repaired_sql = repair_response.choices[0].message.content.strip()

        thinking_log.append("Repaired SQL:")
        thinking_log.append(repaired_sql)

        repaired_result = run_query(repaired_sql)

        if isinstance(repaired_result, str):

            thinking_log.append("Repair failed.")

            return {
                "insight": repaired_result,
                "chart": None,
                "data": None,
                "thinking": thinking_log
            }

        thinking_log.append("Repair successful.")

        chart = select_chart(user_query, repaired_result)

        thinking_log.append(f"Selected chart: {chart}")

        insight = interpret_results(user_query, repaired_sql, repaired_result, market_context)

        thinking_log.append("Insight generated.")

        return {
            "insight": insight,
            "chart": chart,
            "data": repaired_result,
            "thinking": thinking_log
        }

    thinking_log.append("SQL executed successfully.")

    chart = select_chart(user_query, result)

    thinking_log.append(f"Selected chart: {chart}")

    insight = interpret_results(user_query, sql_query, result, market_context)

    thinking_log.append("Insight generated.")

    return {
        "insight": insight,
        "chart": chart,
        "data": result,
        "thinking": thinking_log
    }


# ===================================================
# 🔥 WAR ROOM INTELLIGENCE SYSTEM (MULTI-AGENT)
# ===================================================

# ---------------------------------------------------
# SPECIALIST OPINION AGENT
# ---------------------------------------------------

def specialist_agent(role, question, df):

    prompt = f"""
You are the {role} in a corporate executive war room.

STRICT RULES:
- Max 3 bullet points
- No storytelling
- No explanations
- Speak like a senior executive

Question:
{question}

Data Snapshot:
{df.to_string()}

Return ONLY bullet points.
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# DEBATE AGENT
# ---------------------------------------------------

def debate_agent(question, opinions):

    prompt = f"""
Simulate a HIGH-LEVEL executive debate.

STRICT RULES:
- Short
- Direct
- Realistic tension
- Agents may disagree

Question:
{question}

Expert Opinions:
{opinions}

Return format:

DEBATE HIGHLIGHTS:
(max 5 lines)
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# CONFIDENCE + DISAGREEMENT AGENT
# ---------------------------------------------------

def confidence_agent(question, synthesis):

    prompt = f"""
You are a Decision Intelligence Agent.

STRICT RULES:
Return ONLY:

Confidence: <number>%
Risk Level: Low / Medium / High
Disagreement Level: Low / Medium / High

Question:
{question}

Conclusion:
{synthesis}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# WAR ROOM MASTER ENGINE
# ---------------------------------------------------

def run_war_room(user_query, market_context=None):

    thinking_log = []

    thinking_log.append("War Room activated.")
    thinking_log.append("Generating analytical dataset...")

    sql_query = generate_sql(user_query)
    df = run_query(sql_query)

    if isinstance(df, str):
        return {
            "insight": df,
            "thinking": thinking_log
        }

    thinking_log.append("Dataset prepared.")
    thinking_log.append("Consulting specialist agents...")

    roles = [
        "Growth Strategist",
        "Risk Officer",
        "Finance Controller",
        "Market Intelligence Analyst"
    ]

    opinions = {}

    for role in roles:
        opinions[role] = specialist_agent(role, user_query, df)

    thinking_log.append("Specialist opinions collected.")
    thinking_log.append("Debate engine activated...")

    debate = debate_agent(user_query, opinions)

    thinking_log.append("Debate completed.")
    thinking_log.append("Synthesizing executive conclusion...")

    synthesis = interpret_results(user_query, sql_query, df, market_context)

    confidence = confidence_agent(user_query, synthesis)

    thinking_log.append("Confidence scoring completed.")

    return {
        "insight": synthesis,
        "debate": debate,
        "confidence": confidence,
        "data": df,
        "thinking": thinking_log
    }
