"""
/api/copilot — streaming SSE endpoint for the AI copilot.
Frontend connects via EventSource and receives text tokens as they arrive.
"""
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.rag import retrieve, stream_response

router = APIRouter()


class CopilotRequest(BaseModel):
    query: str
    mode: str = "ops"          # ops | draft | rca
    doc_type: str | None = None  # filter to sops | playbooks | regulatory


async def event_stream(query: str, chunks: list[dict], mode: str):
    """Wrap streamed tokens as SSE events."""
    # First event: send citations so the frontend can render source pills
    sources = list({c["meta"]["title"] for c in chunks})
    yield f"data: [SOURCES]{','.join(sources)}[/SOURCES]\n\n"

    # Stream the response tokens
    async for token in stream_response(query, chunks, mode):
        # Escape newlines for SSE protocol
        safe = token.replace("\n", "\\n")
        yield f"data: {safe}\n\n"

    yield "data: [DONE]\n\n"


@router.post("/stream")
async def copilot_stream(
    req: CopilotRequest,
    x_tenant_id: str = Header(default="demo"),
):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    chunks = await retrieve(req.query, x_tenant_id, req.doc_type)

    if not chunks:
        # No relevant context found — still answer but flag it
        chunks = [{
            "text": "No relevant documents found in the vault for this query.",
            "meta": {"title": "System"},
            "score": 0,
        }]

    return StreamingResponse(
        event_stream(req.query, chunks, req.mode),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disable Nginx buffering
        },
    )


@router.post("/query")
async def copilot_query(
    req: CopilotRequest,
    x_tenant_id: str = Header(default="demo"),
):
    """Non-streaming version — returns full response as JSON. Useful for training mode."""
    chunks = await retrieve(req.query, x_tenant_id, req.doc_type)
    response_text = ""
    async for token in stream_response(req.query, chunks, req.mode):
        response_text += token

    return {
        "response": response_text,
        "sources": [c["meta"]["title"] for c in chunks],
        "chunk_count": len(chunks),
    }
