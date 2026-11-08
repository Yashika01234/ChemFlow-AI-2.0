from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.simulation_service import monte_carlo_yield

router = APIRouter(prefix="/api/simulations", tags=["Monte Carlo"])

class SimulationRequest(BaseModel):
    mean_yield: float = Field(ge=0, le=1)
    std_yield: float = Field(ge=0, le=0.5)
    trials: int = Field(default=5000, ge=100, le=100000)
    seed: int | None = None

@router.post("/monte-carlo")
def simulate(payload: SimulationRequest):
    try:
        return monte_carlo_yield(payload.mean_yield, payload.std_yield, payload.trials, payload.seed)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
