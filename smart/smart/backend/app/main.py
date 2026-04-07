import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field

from app.services.rag_service import get_tutor_response, get_tutor_response_with_context

app = FastAPI(title="Smart Shiksha API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_teacher(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return payload


def create_access_token(payload: Dict[str, Any]) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class ChatMessageRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    language: str = "en"


class ChatMessageResponse(BaseModel):
    session_id: str
    text: str
    audio_url: str
    context_chunks: List[str] = Field(default_factory=list)


class QuizGenerateRequest(BaseModel):
    user_id: str
    weak_topics: List[str] = Field(default_factory=list)


class DashboardStatsResponse(BaseModel):
    progress_vs_time: List[Dict[str, Any]]
    weak_topics: List[str]
    daily_streak: int


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Smart Shiksha API is running"}


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    role = "student"
    if payload.email.lower().endswith("@teacher.smartshiksha.local"):
        role = "teacher"
    elif payload.email.lower().endswith("@admin.smartshiksha.local"):
        role = "admin"

    token = create_access_token({"sub": payload.email, "role": role})
    return LoginResponse(access_token=token, role=role)


@app.post("/chat/message", response_model=ChatMessageResponse)
def chat_message(payload: ChatMessageRequest) -> ChatMessageResponse:
    try:
        answer, context_chunks = get_tutor_response_with_context(payload.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {exc}") from exc

    audio_url = f"/media/tts/{uuid4()}.mp3"
    return ChatMessageResponse(
        session_id=payload.session_id,
        text=answer,
        audio_url=audio_url,
        context_chunks=context_chunks,
    )


@app.get("/dashboard/stats", response_model=DashboardStatsResponse)
def dashboard_stats(user_id: str) -> DashboardStatsResponse:
    sample_series = [
        {"date": "2026-01-20", "score": 61},
        {"date": "2026-01-27", "score": 68},
        {"date": "2026-02-03", "score": 74},
        {"date": "2026-02-07", "score": 79},
    ]
    return DashboardStatsResponse(
        progress_vs_time=sample_series,
        weak_topics=["Algebra", "Chemical Bonding"],
        daily_streak=5,
    )


@app.post("/quiz/generate")
def quiz_generate(payload: QuizGenerateRequest) -> Dict[str, Any]:
    topics = ", ".join(payload.weak_topics) if payload.weak_topics else "general revision"
    quiz_prompt = (
        "Generate a unique 5-question quiz for grade-school students based on these weak topics: "
        f"{topics}. Return concise JSON with question, options, answer, and explanation."
    )

    try:
        quiz_text = get_tutor_response(quiz_prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {exc}") from exc

    return {"user_id": payload.user_id, "quiz": quiz_text}


@app.post("/teacher/upload-curriculum")
async def upload_curriculum(file: UploadFile, token_payload: Dict[str, Any] = Depends(get_current_teacher)) -> Dict[str, str]:
    save_dir = os.getenv("CURRICULUM_UPLOAD_DIR", "backend/data/textbooks")
    os.makedirs(save_dir, exist_ok=True)
    target = os.path.join(save_dir, file.filename)

    content = await file.read()
    with open(target, "wb") as out:
        out.write(content)

    return {
        "message": "File uploaded. Run backend/train_ai.py to update embeddings.",
        "file": target,
    }


@app.get("/health")
def health() -> Dict[str, str]:
    try:
        token = create_access_token({"sub": "healthcheck"})
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=500, detail=f"JWT health failed: {exc}") from exc
    return {"status": "ok"}
