import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        # api_key=os.environ.get("GEMINI_API_KEY"),
        api_key="AIzaSyCMiMoxUqaL5Ew9omhVYPmhmW7UDX600xw",
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
