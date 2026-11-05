import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_intent(text: str) -> str:
   
    text = text.lower()
    if any(w in text for w in ["refund", "money", "payment"]):
        return "billing"
    if any(w in text for w in ["error", "bug", "crash"]):
        return "technical"
    return "general"

def generate_response(user_text: str) -> str:
    intent = detect_intent(user_text)
    prompt = f"""You are a support assistant.
Detected intent: {intent}
User question: {user_text}
Reply clearly in Markdown with a short summary and next steps."""
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(generate_response("I was charged twice for my order, please refund."))