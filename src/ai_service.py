from typing import List
from database import DatabaseManager
from google import genai
from google.genai import types
import traceback
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

config = DatabaseManager.load_settings(SETTINGS_PATH)

api_key = config.get("api_key_google_ai")
client = genai.Client(
    api_key=api_key,
    http_options={'api_version': 'v1'}
)
if not api_key:
    raise ValueError("API Key not found in settings.json")

def get_embedding(text : str) -> List[float]:
    try:
        response = client.models.embed_content(
                model="gemini-embedding-2", 
                contents=text
            )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Some problems with connection to ai embedding {e}.")
        traceback.print_exc()
        return []
    
if __name__ == "__main__":
    test_text = "Nowe zasady ochrony środowiska 2026"
    vector = get_embedding(test_text)
    if vector:
        print(f"Finally! The vector's length: {len(vector)}")
        print(f"First 3 numbers: {vector[:3]}")