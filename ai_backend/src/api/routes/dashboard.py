from fastapi import APIRouter
from typing import Dict, Any


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# PUBLIC_INTERFACE
@router.get("/summary/{user_id}", response_model=Dict[str, Any], summary="Get dashboard summary")
def dashboard_summary(user_id: str):
    """Return a sample dashboard summary (mocked numeric/stat overview)."""
    # In a real impl, would aggregate account, path progress, project stats, etc.
    return {
        "user_id": user_id,
        "total_learning_paths": 2,
        "completed_paths": 1,
        "active_project_ideas": 3,
        "messages_this_week": 7,
        "ui_hint": "Keep up your learning momentum!",
    }
