import os
from groq import Groq
from dotenv import load_dotenv

def get_model_label(model: str) -> str:
    if not model:
        return "llama-3.3-70b-versatile"
    
    model_lower = model.lower()
    
    if model_lower.startswith("gemma"):
        return "gemma2-9b-it"
    elif model_lower.startswith("llama"):
        return "llama-3.3-70b-versatile"
    elif model_lower.startswith("deepseek"):
        return "deepseek-r1-distill-llama-70b"
    elif model_lower.startswith("qwen"):
        return "qwen-qwq-32b"
    
    return  "llama-3.3-70b-versatile"


def chat_with_groq(user_input: str,model) -> str:
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
# gemma2-9b-it , llama-3.3-70b-versatile ,whisper-large-v3 ,distil-whisper-large-v3-en
        model=get_model_label(model),
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

