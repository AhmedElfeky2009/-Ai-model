import os

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Gemini AI Backend")

# قراءة الـ API Key من Render
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found!")

client = genai.Client(api_key=API_KEY)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Gemini Backend is running"
    }


@app.post("/chat")
def chat(data: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=data.message
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }