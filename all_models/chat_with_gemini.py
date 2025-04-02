import os
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv

def chat_with_gemini( prompt: str) -> str:
    # Initialize Gemini client
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Using API key: {api_key}")  # Debugging line to check API key
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash"
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")
    
    # Get response from Gemini model
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text.strip()
