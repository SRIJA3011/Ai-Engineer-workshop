import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS for local testing and future Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # We will restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class ChatIn(BaseModel):
    session_id: str | None = None
    message: str

@app.get("/health")
def health_check():
    # Render requires a health check endpoint
    return {"status": "ok"}

@app.post("/chat")
def chat(payload: ChatIn):
    # Generate session ID if it doesn't exist
    sid = payload.session_id or str(uuid.uuid4())
    
    try:
        # 1. Save user message to Supabase
        supabase.table("chat_messages").insert({
            "session_id": sid,
            "role": "user",
            "content": payload.message
        }).execute()

        # 2. Fetch conversation history from Supabase
        response = supabase.table("chat_messages") \
            .select("role, content") \
            .eq("session_id", sid) \
            .order("created_at") \
            .execute()
        
        history = response.data

        # 3. Send history to Groq
        groq_response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=history
        )
        reply = groq_response.choices[0].message.content

        # 4. Save AI response to Supabase
        supabase.table("chat_messages").insert({
            "session_id": sid,
            "role": "assistant",
            "content": reply
        }).execute()

        return {"session_id": sid, "reply": reply}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new-chat")
def new_chat():
    # Just generate a new session ID
    return {"session_id": str(uuid.uuid4())}