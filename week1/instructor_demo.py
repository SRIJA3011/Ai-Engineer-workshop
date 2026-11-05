import os
from pydantic import BaseModel
from groq import Groq
from instructor import from_groq
from dotenv import load_dotenv

load_dotenv()
client = from_groq(Groq(api_key=os.getenv("GROQ_API_KEY")))

class SupportTicket(BaseModel):
    intent: str
    risk_level: str
    priority: str

result = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    response_model=SupportTicket,
    messages=[{
        "role": "user",
        "content": "My payment was deducted twice. This is urgent and I'm very upset."
    }],
)
print(result.model_dump_json(indent=2))