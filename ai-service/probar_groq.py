import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY", "")
print("Key cargada (primeros 10 caracteres):", api_key[:10])

resp = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": "hola"}],
    },
)

print("Status:", resp.status_code)
print("Body:", resp.text)