from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from rag_engine import get_rag

app = FastAPI(title="Exoplanet Chatbot API")


@app.get("/health")
def health():
    return {"status": "ok"}


# Allow requests from Vercel frontend (and localhost for development)
# Restrict to your specific Vercel URL in production for better security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We will mount static files at the end of the file to ensure API routes are matched first.


class ChatRequest(BaseModel):
    message: str
    language: str = "en-US" # The frontend sends this if we want to explicitly handle it, but LLM handles it well automatically based on input.

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    rag = get_rag()
    
    # We can explicitly ask the LLM to reply in the requested language
    # or just let the LLM infer it from the user's message.
    # To be safe and ensure multi-language works well even if the user says a short phrase:
    prompt_modifier = f" Please reply in the language matching this locale: {req.language}. "
    
    final_query = req.message + prompt_modifier
    
    reply = rag.query(final_query)
    
    return ChatResponse(reply=reply)

# Mount static files at the root
app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
