from fastapi import FastAPI
from app.api import sse  # ✅ sse must have 'router'

app = FastAPI(title="AI Chatbot Backend")

# Include routes
app.include_router(sse.router, prefix="/api")  # ✅ uses sse.router

@app.get("/")
def root():
    return {"message": "Backend is running!"}
