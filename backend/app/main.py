from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import copilot, vault, alerts, training, recon

app = FastAPI(title="OpsCore AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://opscore.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(copilot.router, prefix="/api/copilot", tags=["copilot"])
app.include_router(vault.router,   prefix="/api/vault",   tags=["vault"])
app.include_router(alerts.router,  prefix="/api/alerts",  tags=["alerts"])
app.include_router(training.router,prefix="/api/training",tags=["training"])
app.include_router(recon.router,   prefix="/api/recon",   tags=["recon"])

@app.get("/health")
def health():
    return {"status": "ok"}
