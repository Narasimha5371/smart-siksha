from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.adaptive_learning import AdaptiveLearningEngine

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    user_id = "00000000-0000-0000-0000-000000000001"
    engine = AdaptiveLearningEngine(db)
    recommendations = engine.get_next_recommendations(user_id)
    return [
        {
            "id": str(r.id),
            "title": r.title,
            "subject": r.subject
        }
        for r in recommendations
    ]
