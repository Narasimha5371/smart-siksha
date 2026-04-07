from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.sync import SyncPullResponse, SyncPushRequest
from app.services.sync_service import SyncService
from typing import Optional
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user() -> str:
    # Mock user ID for proto
    return "00000000-0000-0000-0000-000000000001"


@router.get("/pull", response_model=SyncPullResponse)
def pull_changes(
    last_pulled_at: Optional[int] = None,  # Timestamp in seconds or null
    schema_version: int = 1,
    migration: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    last_pulled_dt = None
    if last_pulled_at:
        last_pulled_dt = datetime.fromtimestamp(last_pulled_at)

    service = SyncService(db)
    return service.pull_changes(user_id, last_pulled_dt)


@router.post("/push")
def push_changes(
    payload: SyncPushRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    service = SyncService(db)
    service.push_changes(user_id, payload)
    return {"status": "success"}
