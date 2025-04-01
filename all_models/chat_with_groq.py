import os
from groq import Groq

def chat_with_groq(user_input: str) -> str:
    client = Groq(api_key="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")

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": user_input}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response

