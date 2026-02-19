from core.llm.model_registry import get_client, get_model
from analytics.query_engine import run_query
from core.agents.insight_agent import generate_sql, interpret_results

client = get_client()

# =========================================================
# WAR ROOM INTELLIGENCE SYSTEM
# =========================================================

# ---------------------------------------------------------
# SPECIALIST OPINION AGENT
# ---------------------------------------------------------

def specialist_agent(role, question, df):

    prompt = f"""
You are acting as the {role} in a corporate executive war room.

STRICT RULES:
- Speak like a senior executive
- Max 3 bullet points
- No explanations
- No storytelling
- Focus on business impact

Strategic Question:
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


# ---------------------------------------------------------
# DEBATE ENGINE AGENT
# ---------------------------------------------------------

def debate_agent(question, opinions):

    prompt = f"""
Simulate a HIGH-LEVEL executive debate.

STRICT RULES:
- Short
- Realistic disagreement allowed
- No long explanations
- Reflect tension between growth & risk

Strategic Question:
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


# ---------------------------------------------------------
# CONFIDENCE + DISAGREEMENT AGENT
# ---------------------------------------------------------

def confidence_agent(question, synthesis):

    prompt = f"""
You are a Decision Intelligence Agent.

Evaluate the reliability of this conclusion.

STRICT RULES:
Return ONLY:

Confidence: <number>%
Risk Level: Low / Medium / High
Disagreement Level: Low / Medium / High

Strategic Question:
{question}

Conclusion:
{synthesis}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# RISK vs GROWTH TENSION AGENT
# ---------------------------------------------------------

def tension_agent(question, opinions):

    prompt = f"""
Evaluate strategic tension.

STRICT RULES:
Return ONLY:

Strategic Tension: Low / Medium / High
Primary Conflict: <short phrase>

Strategic Question:
{question}

Opinions:
{opinions}
"""

    response = client.chat.completions.create(
        model=get_model("insight_agent"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# WAR ROOM MASTER ENGINE
# ---------------------------------------------------------

def run_war_room(user_query, market_context=None):

    thinking_log = []

    thinking_log.append("War Room activated.")
    thinking_log.append("Generating strategic dataset...")

    sql_query = generate_sql(user_query)

    thinking_log.append("SQL generated.")
    thinking_log.append(sql_query)

    df = run_query(sql_query)

    if isinstance(df, str):

        thinking_log.append("SQL execution failed.")

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

        thinking_log.append(f"{role} analyzing situation...")

        opinions[role] = specialist_agent(role, user_query, df)

    thinking_log.append("All specialist opinions collected.")
    thinking_log.append("Debate engine activated...")

    debate = debate_agent(user_query, opinions)

    thinking_log.append("Debate completed.")
    thinking_log.append("Synthesizing executive conclusion...")

    synthesis = interpret_results(user_query, sql_query, df, market_context)

    thinking_log.append("Conclusion generated.")
    thinking_log.append("Evaluating decision confidence...")

    confidence = confidence_agent(user_query, synthesis)

    tension = tension_agent(user_query, opinions)

    thinking_log.append("War Room analysis complete.")

    return {
        "insight": synthesis,
        "debate": debate,
        "confidence": confidence,
        "tension": tension,
        "data": df,
        "thinking": thinking_log
    }
