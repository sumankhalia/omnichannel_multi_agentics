from fastapi import APIRouter
from core.agents.intent_agent import IntentAgent
from core.agents.intent_router import IntentRouter

from core.agents.insight_agent import InsightAgent
from core.agents.chart_agent import ChartAgent
from core.agents.churn_agent import ChurnAgent
from core.agents.data_agent import DataAgent
from core.agents.nba_agent import NBAAgent

router = APIRouter()

intent_agent = IntentAgent()
intent_router = IntentRouter()

insight_agent = InsightAgent()
chart_agent = ChartAgent()
churn_agent = ChurnAgent()
data_agent = DataAgent()
nba_agent = NBAAgent()


@router.get("/chat")
def chat(query: str):

    intent = intent_agent.extract_intent(query)

    print("\n🔥 ROUTER RECEIVED INTENT:", intent)

    routing = intent_router.route(intent, query)

    print("🔥 ROUTING DECISION:", routing)

    agent_name = routing.get("agent")

    # -----------------------------
    # CHART AGENT
    # -----------------------------
    if agent_name == "chart_agent":
        chart = chart_agent.generate_chart(query)
        return {"type": "chart", "data": chart}

    # -----------------------------
    # CHURN AGENT
    # -----------------------------
    if agent_name == "churn_agent":
        result = churn_agent.analyze(query)
        return {"type": "analytics", "data": result}

    # -----------------------------
    # DATA AGENT
    # -----------------------------
    if agent_name == "data_agent":
        result = data_agent.analyze(query)
        return {"type": "analytics", "data": result}

    # -----------------------------
    # NBA AGENT
    # -----------------------------
    if agent_name == "nba_agent":
        result = nba_agent.recommend(query)
        return {"type": "action", "data": result}

    # -----------------------------
    # INSIGHT AGENT (DEFAULT)
    # -----------------------------
    insight = insight_agent.generate_insight(query)
    return {"type": "insight", "data": insight}
