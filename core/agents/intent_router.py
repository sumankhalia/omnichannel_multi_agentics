class IntentRouter:

    def route(self, intent, query=None):

        intent_type = intent.get("type")

        print("\n🔥 INTENT ROUTER ACTIVE")
        print("Intent Type:", intent_type)

        # -----------------------------
        # CHART REQUESTS
        # -----------------------------
        if intent_type == "chart":
            print("Routing → chart_agent ✅")
            return {"agent": "chart_agent"}

        # -----------------------------
        # ACTION REQUESTS
        # -----------------------------
        if intent_type == "action":
            print("Routing → nba_agent ✅")
            return {"agent": "nba_agent"}

        # -----------------------------
        # ANALYTICS REQUESTS
        # -----------------------------
        if intent_type == "analytics":

            if query:
                query_lower = query.lower()

                if "churn" in query_lower:
                    print("Routing → churn_agent ✅")
                    return {"agent": "churn_agent"}

                if "revenue" in query_lower or "sales" in query_lower:
                    print("Routing → data_agent ✅")
                    return {"agent": "data_agent"}

            print("Routing → data_agent (fallback) ✅")
            return {"agent": "data_agent"}

        # -----------------------------
        # DEFAULT → INSIGHT
        # -----------------------------
        print("Routing → insight_agent ✅")
        return {"agent": "insight_agent"}
