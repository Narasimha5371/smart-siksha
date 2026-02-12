import sys
import os
import random
import uuid
from datetime import datetime, timedelta

# Add backend directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.all_models import User, UserRole, Lesson, StudentProgress, ProgressStatus

def seed_data():
    db = SessionLocal()
    
    # Drop all tables and recreate (Fresh start for migration)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 1. Create a few Lessons
    lessons = []
    subjects = ["Math", "Physics", "Chemistry"]
    for i in range(10):
        lesson = Lesson(
            id=uuid.uuid4(),
            subject=random.choice(subjects),
            grade=10,
            title=f"Lesson {i+1}: {random.choice(['Algebra', 'Newton laws', 'Organic Chem', 'Calculus'])}",
            content_hash="hash",
            download_url="http://example.com",
            complexity_level=random.random()
        )
        db.add(lesson)
        lessons.append(lesson)
    db.commit()

    # 2. Create Students
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari"]
    last_names = ["Patel", "Sharma", "Gupta", "Singh", "Kumar", "Iyer", "Reddy", "Nair", "Verma", "Mehta"]
    
    students = []
    for i in range(50):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        student = User(
            id=uuid.uuid4(),
            username=f"student{i}",
            hashed_password="hashed_password",
            role=UserRole.STUDENT,
            last_synced_at=datetime.utcnow() - timedelta(days=random.randint(0, 5))
        )
        db.add(student)
        students.append(student)
    
    db.commit()

    # 3. Create Progress (Mock Data)
    for student in students:
        # Each student has done 2-5 lessons
        completed_count = random.randint(2, 5)
        for _ in range(completed_count):
            lesson = random.choice(lessons)
            progress = StudentProgress(
                id=uuid.uuid4(),
                student_id=student.id,
                lesson_id=lesson.id,
                status=ProgressStatus.COMPLETED,
                score=random.randint(40, 100),
                attempts=random.randint(1, 3),
                updated_at=datetime.utcnow()
            )
            db.add(progress)
            
    db.commit()
    db.close()
    print("PostgreSQL Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
