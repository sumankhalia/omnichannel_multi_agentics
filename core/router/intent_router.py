class IntentRouter:

    def route(self, intent, query=None):

        intent_type = intent.get("type")

        # -----------------------------
        # CHART REQUESTS
        # -----------------------------
        if intent_type == "chart":
            return {
                "agent": "chart_agent",
                "action": "generate_chart"
            }

        # -----------------------------
        # ANALYTICS REQUESTS
        # -----------------------------
        if intent_type == "analytics":

            if query:
                query_lower = query.lower()

                if "churn" in query_lower:
                    return {
                        "agent": "insight_agent",   # ← FIXED
                        "action": "generate_insight"
                    }

                if "revenue" in query_lower:
                    return {
                        "agent": "data_agent",
                        "action": "analyze_revenue"
                    }

            return {
                "agent": "data_agent",
                "action": "general_analytics"
            }

        # -----------------------------
        # ACTION REQUESTS
        # -----------------------------
        if intent_type == "action":
            return {
                "agent": "nba_agent",
                "action": "recommend_strategy"
            }

        # -----------------------------
        # DEFAULT → INSIGHT
        # -----------------------------
        return {
            "agent": "insight_agent",
            "action": "generate_insight"
        }
