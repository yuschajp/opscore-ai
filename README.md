# OpsCore AI

**AI-powered operations copilot for capital markets teams.**

OpsCore AI combines a structured knowledge vault of SOPs, playbooks, and regulatory content with Claude-powered natural language Q&A, root cause analysis, and document drafting. Built for hedge fund and asset management operations teams.

→ Live demo: [opscore-demo.vercel.app](https://opscore-demo.vercel.app) *(coming soon)*
→ Portfolio: [joseph-yuschak.notion.site](https://joseph-yuschak.notion.site)

---

## What it does

- **Copilot Q&A** — Ask plain-English questions about trade lifecycle, settlement procedures, margin calls, and clearing; get cited answers grounded in your firm's own SOPs.
- **Root cause analysis** — Describe a break or exception; the AI reasons step-by-step to a likely cause and resolution path.
- **Document drafting** — Generate or improve SOPs, escalation memos, and client communications consistent with existing procedures.
- **Regulatory alerts** — Automated weekly summaries of SEC and CFTC releases translated into operational impact for ops teams.
- **Training mode** — AI-generated quiz questions from your own playbooks for new hire onboarding.

---

## Tech stack

| Layer | Technology |
|---|---|
| AI / LLM | Anthropic Claude (claude-sonnet-4-6), streaming SSE |
| RAG / embeddings | OpenAI text-embedding-3-small, ChromaDB |
| Backend | Python, FastAPI, LangChain |
| Database | PostgreSQL (breaks log, alerts, users), Redis (session) |
| Frontend | Next.js 14, Tailwind CSS |
| Infrastructure | Railway (API), Vercel (frontend), AWS S3 (vault storage) |
| Auth | Clerk (multi-tenant, SSO) |

---

## Project structure

```
opscore-ai/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app
│   │   ├── api/
│   │   │   ├── copilot.py        # Streaming SSE copilot endpoint
│   │   │   ├── vault.py          # SOP/playbook CRUD
│   │   │   ├── alerts.py         # Regulatory alert feed
│   │   │   ├── training.py       # Quiz generation and scoring
│   │   │   └── recon.py          # Break dashboard data
│   │   ├── core/
│   │   │   ├── rag.py            # Embed → retrieve → stream pipeline
│   │   │   └── reg_alerts.py     # SEC/CFTC RSS fetch + Claude summarization
│   │   └── ingestion/
│   │       └── ingest.py         # Vault ingestion pipeline
│   ├── vault/
│   │   ├── sops/                 # Standard operating procedures
│   │   ├── playbooks/            # Workflow playbooks
│   │   └── regulatory/           # Regulatory summaries
│   └── requirements.txt
├── frontend/                     # Next.js app (see /frontend/README.md)
└── scripts/                      # Standalone Python utilities
```

---

## Quickstart

```bash
# Clone and install
git clone https://github.com/yuschajp/opscore-ai
cd opscore-ai/backend
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add: ANTHROPIC_API_KEY, OPENAI_API_KEY

# Ingest the starter vault
python -m app.ingestion.ingest --tenant demo --vault ./vault

# Start the API server
uvicorn app.main:app --reload --port 8000
```

---

## Knowledge vault

The vault ships with production-quality SOPs written from 15 years of hedge fund operations experience:

- **Equity Trade Settlement and DK Resolution** (SEC Rule 15c6-1, T+2 cycle, DTCC buy-in procedures)
- **Futures Margin Call Escalation Playbook** (VM/IM/intraday, LME broken dates, FCM dispute resolution)
- *(More SOPs added weekly — see vault/sops/)*

---

## Roadmap

- [x] Core RAG engine with streaming citations
- [x] Equity settlement SOP
- [x] Futures margin SOP
- [x] Regulatory alert engine (SEC + CFTC RSS)
- [ ] Next.js frontend with SSE streaming
- [ ] Training mode quiz generator
- [ ] Recon dashboard with synthetic break data
- [ ] Real prime broker CSV ingest (V2)
- [ ] Slack /opscore slash command (V2)
- [ ] Self-hosted Docker deployment option (V2)

---

## Author

**Joseph Yuschak** — Capital markets operations and technology professional.
15+ years at Millennium Management, Schonfeld Strategic Advisors, F&G Annuities, and Fannie Mae.

→ [joseph-yuschak.notion.site](https://joseph-yuschak.notion.site) | [github.com/yuschajp](https://github.com/yuschajp)
