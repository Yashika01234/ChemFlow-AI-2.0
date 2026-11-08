from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import json
from app.services.compound_service import analyze_compound, classify_organic
from app.db import save_history

router = APIRouter(prefix="/api", tags=["Compounds"])

class CompoundRequest(BaseModel):
    smiles: str = Field(min_length=1, max_length=500)
    name: str | None = None

class OrganicRequest(BaseModel):
    reactants: list[str] = Field(min_length=1, max_length=8)

@router.post("/compounds/analyze")
def compound_analysis(payload: CompoundRequest):
    try:
        result = analyze_compound(payload.smiles)
        result["name"] = payload.name
        save_history("compound", payload.smiles, json.dumps(result))
        return result
    except ValueError as exc:
        raise HTTPException(422, str(exc))

@router.post("/organic/classify")
def organic_classification(payload: OrganicRequest):
    try:
        result = classify_organic(payload.reactants)
        save_history("organic", ",".join(payload.reactants), json.dumps(result))
        return result
    except ValueError as exc:
        raise HTTPException(422, str(exc))
