import openai
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_answer(query: str, context: list, history: list = []):
    messages = [
        {"role": "system", "content": "Answer only based on provided context. If unsure, say 'I don't know.'"},
        *history,
        {"role": "user", "content": f"Query: {query}\n\nContext:\n{''.join(context)}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message['content']
