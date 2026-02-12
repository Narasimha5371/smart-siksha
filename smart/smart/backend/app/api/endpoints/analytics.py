from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.all_models import User, UserRole, StudentProgress
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DashboardStats(BaseModel):
    avg_class_score: int
    active_students: int
    total_students: int
    tests_completed: int

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Total Students
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    
    # Active Students (mock logic: synced at least once)
    active_students = db.query(User).filter(
        User.role == UserRole.STUDENT, 
        User.last_synced_at.isnot(None)
    ).count()

    # Tests Completed & Avg Score
    all_progress = db.query(StudentProgress).all()
    tests_completed = len(all_progress)
    
    avg_class_score = 0
    if all_progress:
        total_score = sum(p.score for p in all_progress)
        avg_class_score = int(total_score / len(all_progress))

    return DashboardStats(
        avg_class_score=avg_class_score,
        active_students=active_students,
        total_students=total_students,
        tests_completed=tests_completed
    )
