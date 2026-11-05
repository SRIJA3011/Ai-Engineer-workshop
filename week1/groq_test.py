import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
   model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Say 'Groq API connected' in 4 words."}],
)
print(resp.choices[0].message.content)