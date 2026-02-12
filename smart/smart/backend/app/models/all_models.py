from sqlalchemy import Column, String, Enum, DateTime, Integer, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base
import enum

def generate_uuid():
    return uuid.uuid4()

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_synced_at = Column(DateTime, nullable=True)

    progress = relationship("StudentProgress", back_populates="student")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    subject = Column(String, index=True)
    grade = Column(Integer)
    title = Column(String)
    content_hash = Column(String) # For checksums
    download_url = Column(String)
    complexity_level = Column(Float, default=0.5)
    prerequisite_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=True)

class ProgressStatus(str, enum.Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    COMPLETED = "completed"

class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.LOCKED)
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="progress")
    lesson = relationship("Lesson")

class Curriculum(Base):
    __tablename__ = "curriculum"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    description = Column(String)
    grade = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Performance(Base):
    __tablename__ = "performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    subject = Column(String, index=True)
    average_score = Column(Float, default=0.0)
    total_attempts = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user_message = Column(String)
    ai_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("User")

class LearningPath(Base):
    __tablename__ = "learning_path"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    path_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User")
