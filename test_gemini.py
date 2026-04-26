import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence"
)

print("SUCCESS! Gemini says:")
print(response.text)