from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.all_models import User, UserRole

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserListResponse(BaseModel):
    id: str
    username: str
    role: str
    last_active: Optional[str] = "Never"
    avg_score: int

@router.get("/", response_model=List[UserListResponse])
def get_users(role: UserRole = UserRole.STUDENT, db: Session = Depends(get_db)):
    users = db.query(User).options(selectinload(User.progress)).filter(User.role == role).all()

    response = []
    for user in users:
        # Calculate stats on the fly (for MVP)
        progress = user.progress

        avg_score = 0
        if progress:
            total_score = sum(p.score for p in progress)
            avg_score = int(total_score / len(progress))

        last_active = "Never"
        if user.last_synced_at:
            # Simple formatting
            last_active = user.last_synced_at.strftime("%Y-%m-%d %H:%M")

        response.append(UserListResponse(
            id=str(user.id),
            username=user.username,
            role=user.role,
            last_active=last_active,
            avg_score=avg_score
        ))

    return response
