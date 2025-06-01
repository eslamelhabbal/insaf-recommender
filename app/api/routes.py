from fastapi import APIRouter
from app.logic.recommender import get_recommended_suppliers

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Recommendation API is running"}


@router.get("/recommend/{charity_id}")
def recommend_suppliers(charity_id: int):
    result = get_recommended_suppliers(charity_id)
    return result
