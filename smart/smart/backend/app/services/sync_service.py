from sqlalchemy.orm import Session
from app.models.all_models import StudentProgress, User
from app.schemas.sync import SyncPushRequest
from datetime import datetime
from typing import Dict, List, Any

class SyncService:
    def __init__(self, db: Session):
        self.db = db

    def pull_changes(self, user_id: str, last_pulled_at: datetime | None):
        """
        Fetch changes since last_pulled_at.
        For WatermelonDB compatibility, we return created/updated/deleted.
        Currently assuming Soft Deletes are not fully implemented, only Updates.
        """
        # Fetch updated progress
        query = self.db.query(StudentProgress).filter(StudentProgress.student_id == user_id)
        
        if last_pulled_at:
            query = query.filter(StudentProgress.updated_at > last_pulled_at)
        
        changed_progress = query.all()

        return {
            "changes": {
                "student_progress": {
                    "created": [], # For simplicity in this V1, treating all as updated or determining based on created_at could be done
                    "updated": [p.__dict__ for p in changed_progress], 
                    "deleted": []
                }
            },
            "timestamp": datetime.utcnow()
        }

    def push_changes(self, user_id: str, payload: SyncPushRequest):
        """
        Apply changes from the client to the server.
        """
        changes = payload.changes
        
        # Handle Student Progress Changes
        if "student_progress" in changes:
            progress_changes = changes["student_progress"]
            
            # handle created
            for item in progress_changes.get("created", []):
                # Ensure we don't duplicate if ID exists (idempotency)
                existing = self.db.query(StudentProgress).filter(StudentProgress.id == item['id']).first()
                if not existing:
                    new_record = StudentProgress(**item)
                    # Force student_id validation
                    new_record.student_id = user_id 
                    self.db.add(new_record)
            
            # handle updated
            updated_items = progress_changes.get("updated", [])
            if updated_items:
                updated_ids = [item['id'] for item in updated_items]
                existing_records = self.db.query(StudentProgress).filter(StudentProgress.id.in_(updated_ids)).all()
                existing_map = {str(record.id): record for record in existing_records}

                for item in updated_items:
                    existing = existing_map.get(str(item['id']))
                    if existing:
                        # Generic update
                        for key, value in item.items():
                            if hasattr(existing, key):
                                setattr(existing, key, value)
                        existing.updated_at = datetime.utcnow()

        self.db.commit()
