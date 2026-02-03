import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print("--- AVAILABLE MODELS ---")
    try:
        # In the new SDK, we just iterate and print the name directly
        for model in client.models.list():
            print(f"Found: {model.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()