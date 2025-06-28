from fastapi import APIRouter
from typing import List
from ..schemas import (
    LearningPathSchema,
    LearningPathCreateRequest,
)
from ..services.learning_path import (
    generate_mock_learning_path,
    create_learning_path,
    get_mock_learning_paths_for_user,
)


router = APIRouter(
    prefix="/learning-paths",
    tags=["Learning Paths"],
)


# PUBLIC_INTERFACE
@router.post("/", response_model=LearningPathSchema, summary="Create custom learning path")
def create_custom_learning_path(request: LearningPathCreateRequest):
    """Create a personalized learning path from user input (mock implementation)."""
    path = create_learning_path(request)
    return path


# PUBLIC_INTERFACE
@router.get(
    "/{user_id}",
    response_model=List[LearningPathSchema],
    summary="Get user learning paths",
)
def get_learning_paths(user_id: str):
    """Get sample/mock learning paths for a user."""
    return get_mock_learning_paths_for_user(user_id)


# PUBLIC_INTERFACE
@router.get(
    "/mock/sample/{user_id}",
    response_model=LearningPathSchema,
    summary="Get a sample generated learning path",
)
def mock_generate_path(user_id: str):
    """Generate a demo learning path for a user (single path)."""
    return generate_mock_learning_path(user_id)
