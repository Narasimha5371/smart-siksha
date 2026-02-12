from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class SyncPullRequest(BaseModel):
    last_pulled_at: Optional[datetime] = None
    schema_version: int = 1
    migration: Any = None # Reserved for future migrations

class SyncPullResponse(BaseModel):
    changes: Dict[str, Dict[str, List[Any]]] # {table_name: {created: [], updated: [], deleted: []}}
    timestamp: datetime

class SyncPushRequest(BaseModel):
    changes: Dict[str, Dict[str, List[Dict[str, Any]]]] # {table_name: {created: [], updated: [], deleted: []}}
    last_pulled_at: datetime
