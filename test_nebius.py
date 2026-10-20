import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
    raise SystemExit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api.tokenfactory.nebius.com/v1",
)

try:
    models = client.models.list()
    print("Connection successful!")
    print("Models available to this key:", len(models.data))
    print("Check completed without displaying your API key.")
except Exception as error:
    print("Connection check failed:", type(error).__name__)
    print("Check your key, account access, and network connection.")
    