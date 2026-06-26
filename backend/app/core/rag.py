"""
RAG engine: embed query → vector search → build context → stream Claude response.
This is the heart of OpsCore AI.
"""
import os
from typing import AsyncGenerator
import anthropic
import chromadb
from openai import AsyncOpenAI

ANTHROPIC_CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
OPENAI_CLIENT    = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL      = "text-embedding-3-small"
CLAUDE_MODEL     = "claude-sonnet-4-6"
TOP_K            = 5

# Chroma runs locally in V1; swap to Qdrant Cloud for enterprise
_chroma = chromadb.PersistentClient(path="./chroma_db")

def get_collection(tenant_id: str):
    """One Chroma collection per tenant — keeps knowledge vaults isolated."""
    return _chroma.get_or_create_collection(
        name=f"vault_{tenant_id}",
        metadata={"hnsw:space": "cosine"},
    )

async def embed(text: str) -> list[float]:
    resp = await OPENAI_CLIENT.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding

async def retrieve(query: str, tenant_id: str, doc_type: str | None = None) -> list[dict]:
    """Vector search with optional doc_type filter (sop | playbook | regulatory)."""
    collection = get_collection(tenant_id)
    where = {"doc_type": doc_type} if doc_type else None

    results = collection.query(
        query_embeddings=[await embed(query)],
        n_results=TOP_K,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if dist < 0.7:  # cosine distance threshold — tune per corpus
            chunks.append({"text": doc, "meta": meta, "score": 1 - dist})
    return chunks

# ── System prompts per mode ────────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "ops": """You are OpsCore AI, a capital markets operations expert assistant.
You help operations professionals at hedge funds, asset managers, and prime brokers
answer questions about trade lifecycle, reconciliation, margin, clearing, and regulatory compliance.

ALWAYS:
- Base answers on the retrieved context chunks provided. Cite the source document by name.
- Be precise. Ops teams act on your answers — ambiguity causes breaks.
- Flag when a question falls outside the retrieved context rather than guessing.
- Use regulatory rule numbers (e.g. SEC Rule 15c6-1) when they appear in the context.

Format citations as: [Source: {document_title}]
""",

    "draft": """You are OpsCore AI in document drafting mode.
Help the user write or improve operational documents: SOPs, escalation procedures,
memos, email templates, and client communications.
Use the retrieved context to ensure drafts are consistent with existing procedures.
Output clean, professional prose ready to copy into a document.
""",

    "rca": """You are OpsCore AI in root cause analysis mode.
Help the user diagnose trade breaks, fails, and operational exceptions.
Reason step by step: (1) identify the break type, (2) list likely causes in order of probability,
(3) state what data to check first, (4) recommend resolution path.
Cite relevant SOPs or regulatory requirements from the retrieved context.
""",
}

async def stream_response(
    query: str,
    chunks: list[dict],
    mode: str = "ops",
) -> AsyncGenerator[str, None]:
    """Stream a Claude response given retrieved chunks. Yields text tokens."""

    context_block = "\n\n---\n".join(
        f"[Source: {c['meta'].get('title', 'Unknown')}]\n{c['text']}"
        for c in chunks
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"<retrieved_context>\n{context_block}\n</retrieved_context>\n\n"
                f"Question: {query}"
            ),
        }
    ]

    with ANTHROPIC_CLIENT.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["ops"]),
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
