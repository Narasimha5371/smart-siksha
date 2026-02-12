from sqlalchemy.orm import Session
from app.models.all_models import StudentProgress, Lesson, ProgressStatus
import random

class AdaptiveLearningEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_next_recommendations(self, student_id: str, limit: int = 3):
        """
        Recommend next lessons based on:
        1. Prerequisite completion
        2. Current capability level vs Lesson complexity
        """
        # 1. Get completed lessons to determine satisfied prerequisites
        completed = self.db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id,
            StudentProgress.status == ProgressStatus.COMPLETED
        ).all()
        completed_ids = [str(p.lesson_id) for p in completed]

        # 2. Find eligible lessons (Prerequisites met, not yet completed)
        # In a real app, this query would be more optimized
        all_lessons = self.db.query(Lesson).all()
        
        eligible_lessons = []
        for lesson in all_lessons:
            if str(lesson.id) in completed_ids:
                continue
            
            # Check prerequisite
            if lesson.prerequisite_id:
                if str(lesson.prerequisite_id) not in completed_ids:
                    continue # Prereq not met
            
            eligible_lessons.append(lesson)

        # 3. Sort/Rank by complexity or other factors
        # For V1: Simple sort by complexity
        eligible_lessons.sort(key=lambda x: x.complexity_level)

        return eligible_lessons[:limit]

    def update_student_capability(self, student_id: str, quiz_score: int):
        """
        A simple hook to adjust internal student metrics if we had them.
        For now, this just acknowledges the score.
        """
        pass
