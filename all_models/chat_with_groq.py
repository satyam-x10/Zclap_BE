import os
from groq import Groq
from dotenv import load_dotenv

def chat_with_groq(user_input: str) -> str:
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

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

