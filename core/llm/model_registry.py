from openai import OpenAI
import os

MODEL_CONFIG = {
    "insight_agent": "gpt-5-mini",
    "sql_agent": "gpt-5-mini",
    "prediction_agent": "gpt-5-mini",
}

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model(agent_name):
    return MODEL_CONFIG.get(agent_name, "gpt-5-mini")
