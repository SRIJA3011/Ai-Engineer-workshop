import os, uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


sessions: dict[str, list[dict]] = {}

class ChatIn(BaseModel):
    session_id: str | None = None
    message: str

@app.post("/chat")
def chat(payload: ChatIn):
    sid = payload.session_id or str(uuid.uuid4())
    history = sessions.setdefault(sid, [])
    history.append({"role": "user", "content": payload.message})

    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=history,
    )
    reply = resp.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    return {"session_id": sid, "reply": reply}

@app.post("/new-chat")
def new_chat():
    return {"session_id": str(uuid.uuid4())}