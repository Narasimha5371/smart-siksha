from fastapi import APIRouter

api_router = APIRouter()

from app.api.endpoints import sync, learning, users, analytics

api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

