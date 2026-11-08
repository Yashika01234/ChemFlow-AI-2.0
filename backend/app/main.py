from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db, get_history
from app.api.routes import compounds, reactions, stoichiometry, simulations

app = FastAPI(
    title="ChemFlow AI 2.0 API",
    description="Chemistry intelligence services: compounds, organic chemistry, reaction templates, stoichiometry and uncertainty simulation.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "service": "ChemFlow AI 2.0"}

@app.get("/api/history", tags=["System"])
def history(limit: int = 20):
    return get_history(max(1, min(limit, 100)))

app.include_router(compounds.router)
app.include_router(reactions.router)
app.include_router(stoichiometry.router)
app.include_router(simulations.router)
