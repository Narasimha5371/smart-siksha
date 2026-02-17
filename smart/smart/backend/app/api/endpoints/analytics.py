from fastapi import APIRouter, Depends
from sqlalchemy import func
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
    progress_stats = db.query(
        func.count(StudentProgress.id),
        func.avg(StudentProgress.score)
    ).first()

    tests_completed = progress_stats[0]
    avg_class_score = int(progress_stats[1]) if progress_stats[1] is not None else 0

    return DashboardStats(
        avg_class_score=avg_class_score,
        active_students=active_students,
        total_students=total_students,
        tests_completed=tests_completed
    )
