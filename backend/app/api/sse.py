# app/api/sse.py
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.providers.gemini_adapter import query_gemini
import json

router = APIRouter()  # ✅ must exist exactly like this

@router.get("/chat")
async def chat(prompt: str, level: int | None = Query(None, ge=1, le=3)):
    def event_stream():
        # query_gemini returns a full string; send as a single SSE event
        result = query_gemini(prompt, level=level)
        # If someday query_gemini yields chunks, we can iterate; for now just one event
        yield f"data: {json.dumps({'response': result})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
