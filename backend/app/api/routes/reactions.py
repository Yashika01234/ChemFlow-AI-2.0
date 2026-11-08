from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.reaction_service import predict_products

router = APIRouter(prefix="/api/reactions", tags=["Reaction prediction"])

class ReactionRequest(BaseModel):
    reaction: str
    reactants: list[str] = Field(min_length=1, max_length=4)

@router.post("/predict")
def reaction_prediction(payload: ReactionRequest):
    try:
        return predict_products(payload.reaction, payload.reactants)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
