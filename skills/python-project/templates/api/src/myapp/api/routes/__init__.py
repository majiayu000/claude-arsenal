"""API routes aggregation."""

from fastapi import APIRouter

from myapp.api.routes import user

router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["users"])
