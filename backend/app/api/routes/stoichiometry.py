from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.stoichiometry_service import balance_equation, limiting_reagent

router = APIRouter(prefix="/api/stoichiometry", tags=["Stoichiometry"])

class BalanceRequest(BaseModel):
    equation: str = Field(min_length=3, max_length=500)

class YieldRequest(BaseModel):
    reactant_moles: dict[str, float]
    reactant_coefficients: dict[str, float]
    product_coefficient: float = Field(gt=0)
    product_molar_mass: float = Field(gt=0)

@router.post("/balance")
def balance(payload: BalanceRequest):
    try:
        return balance_equation(payload.equation)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

@router.post("/yield")
def yield_estimate(payload: YieldRequest):
    try:
        return limiting_reagent(payload.reactant_moles, payload.reactant_coefficients,
                                payload.product_coefficient, payload.product_molar_mass)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
