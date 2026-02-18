class IntentAgent:

    def extract_intent(self, query):

        query_lower = query.lower()

        print("\nINTENT AGENT ACTIVE")
        print("Query:", query_lower)

        # -----------------------------
        # CHART INTENT
        # -----------------------------
        chart_words = ["chart", "graph", "plot", "visual", "visualize"]

        for word in chart_words:
            if word in query_lower:
                print("Intent → chart ✅")
                return {"type": "chart"}

        # -----------------------------
        # ACTION INTENT
        # -----------------------------
        action_words = ["strategy", "recommend", "should", "action"]

        for word in action_words:
            if word in query_lower:
                print("Intent → action ✅")
                return {"type": "action"}

        # -----------------------------
        # ANALYTICS INTENT
        # -----------------------------
        analytics_words = ["churn", "revenue", "sales", "analysis"]

        for word in analytics_words:
            if word in query_lower:
                print("Intent → analytics ✅")
                return {"type": "analytics"}

        print("Intent → insight ✅")
        return {"type": "insight"}
