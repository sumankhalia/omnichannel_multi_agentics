from openai import OpenAI

client = OpenAI()


def query_llm(prompt):

    print("\nLLM CLIENT ACTIVE")
    print("Prompt:", prompt)

    try:

        response = client.responses.create(
            model="gpt-5-mini",   # cheap + perfect for accelerator
            input=prompt
        )

        return response.output_text

    except Exception as e:

        print("LLM Error:", str(e))
        return "Insight engine unavailable"
