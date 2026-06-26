"""
Ingestion pipeline: walks the vault directory, chunks markdown files,
embeds via OpenAI, and upserts to ChromaDB.

Run: python -m app.ingestion.ingest --tenant demo --vault ./vault
"""
import argparse
import hashlib
import os
import re
from pathlib import Path

import chromadb
from openai import OpenAI

EMBED_MODEL  = "text-embedding-3-small"
CHUNK_SIZE   = 512    # tokens (approx — we split on words)
CHUNK_OVERLAP = 64

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
chroma_client = chromadb.PersistentClient(path="./chroma_db")


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_markdown(text: str, title: str) -> list[str]:
    """
    Smart chunker for procedural SOPs:
    - Preserves numbered steps within the same chunk where possible
    - Splits on section headers (##) as natural boundaries
    - Falls back to word-count splitting with overlap
    """
    # Split on H2/H3 headers first — these are natural SOP sections
    sections = re.split(r"\n(?=#{2,3} )", text)
    chunks = []

    for section in sections:
        words = section.split()
        if len(words) <= CHUNK_SIZE:
            chunks.append(section.strip())
        else:
            # Slide window with overlap
            for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
                chunk = " ".join(words[i : i + CHUNK_SIZE])
                chunks.append(chunk)

    return [c for c in chunks if len(c.strip()) > 50]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML-like frontmatter from markdown files."""
    meta = {}
    if not text.startswith("---"):
        return meta, text

    end = text.find("---", 3)
    if end == -1:
        return meta, text

    frontmatter = text[3:end].strip()
    for line in frontmatter.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()

    return meta, text[end + 3:].strip()


# ── Embedding ─────────────────────────────────────────────────────────────────

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed up to 100 chunks in one API call."""
    resp = openai_client.embeddings.create(input=texts, model=EMBED_MODEL)
    return [r.embedding for r in resp.data]


# ── Ingest ────────────────────────────────────────────────────────────────────

def ingest_vault(vault_dir: str, tenant_id: str):
    collection = chroma_client.get_or_create_collection(
        name=f"vault_{tenant_id}",
        metadata={"hnsw:space": "cosine"},
    )

    vault_path = Path(vault_dir)
    md_files = list(vault_path.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files in {vault_dir}")

    all_chunks, all_ids, all_metas = [], [], []

    for filepath in md_files:
        raw = filepath.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(raw)

        # Infer doc_type from subfolder (sops/ playbooks/ regulatory/)
        relative = filepath.relative_to(vault_path)
        doc_type = relative.parts[0] if len(relative.parts) > 1 else "general"

        title = frontmatter.get("title", filepath.stem.replace("-", " ").title())
        domain = frontmatter.get("domain", "general")
        updated = frontmatter.get("updated", "")

        chunks = chunk_markdown(body, title)
        print(f"  {filepath.name}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.md5(f"{filepath}:{i}".encode()).hexdigest()
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metas.append({
                "title":    title,
                "doc_type": doc_type,
                "domain":   domain,
                "updated":  updated,
                "filepath": str(filepath),
                "chunk_idx": i,
            })

    # Embed in batches of 100
    batch_size = 100
    all_embeddings = []
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        print(f"Embedding batch {i // batch_size + 1} ({len(batch)} chunks)...")
        all_embeddings.extend(embed_batch(batch))

    # Upsert to Chroma
    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        embeddings=all_embeddings,
        metadatas=all_metas,
    )
    print(f"\nDone. {len(all_chunks)} chunks upserted to vault_{tenant_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest vault into ChromaDB")
    parser.add_argument("--tenant", default="demo", help="Tenant ID")
    parser.add_argument("--vault",  default="./vault", help="Path to vault directory")
    args = parser.parse_args()

    ingest_vault(args.vault, args.tenant)
