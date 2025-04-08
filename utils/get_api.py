# utils/gpt_api.py
import openai

def query_gpt(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"
