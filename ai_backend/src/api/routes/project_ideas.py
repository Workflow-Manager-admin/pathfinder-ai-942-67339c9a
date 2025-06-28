from fastapi import APIRouter
from typing import List
from ..schemas import (
    ProjectIdeaSchema,
    ProjectIdeaGenerateRequest,
)
from ..services.project_ideas import (
    generate_mock_project_ideas,
    get_generic_project_ideas,
)


router = APIRouter(
    prefix="/project-ideas",
    tags=["Project Ideas"],
)


# PUBLIC_INTERFACE
@router.post(
    "/generate",
    response_model=List[ProjectIdeaSchema],
    summary="Generate personalized project ideas",
)
def generate_project_ideas(request: ProjectIdeaGenerateRequest):
    """Generate project ideas personalized to the user (mock/AI stub)."""
    return generate_mock_project_ideas(request)


# PUBLIC_INTERFACE
@router.get(
    "/generic",
    response_model=List[ProjectIdeaSchema],
    summary="Generic project ideas",
)
def list_generic_project_ideas():
    """Return non-personalized project ideas."""
    return get_generic_project_ideas()
