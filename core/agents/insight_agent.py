from core.llm.openai_client import query_llm


class InsightAgent:

    def generate_insight(self, query):

        print("\nINSIGHT AGENT ACTIVE")
        print("Query:", query)

        try:
            response = query_llm(query)

            #Defensive Guard (CRITICAL)
            if not response:
                return {
                    "type": "insight",
                    "data": "No insight generated"
                }

            return {
                "type": "insight",
                "data": response
            }

        except Exception as e:

            print("🔥 Insight Agent Error:", str(e))

            return {
                "type": "insight",
                "data": "Insight engine encountered an error"
            }
