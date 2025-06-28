from fastapi import APIRouter, HTTPException
from ..schemas import (
    OnboardingDataSchema,
    OnboardingDataCreateRequest,
    UserProfileSchema,
    UserProfileCreateRequest,
    UserProfileUpdateRequest,
)
from ..models import OnboardingData, UserProfile
from uuid import uuid4
from datetime import datetime


router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"],
)

# In-memory mock persistence for this MVP
MOCK_USER_DB = {}
MOCK_ONBOARDING_DB = {}


# PUBLIC_INTERFACE
@router.post("/profile", response_model=UserProfileSchema, summary="Create user profile")
def create_user_profile(request: UserProfileCreateRequest):
    """Create a new user profile (mocked, NOT persistent)."""
    user_id = str(uuid4())
    now = datetime.utcnow()
    profile = UserProfile(
        user_id=user_id,
        name=request.name,
        email=request.email,
        bio=request.bio,
        avatar_url=request.avatar_url,
        interests=request.interests,
        role=request.role,
        created_at=now,
    )
    MOCK_USER_DB[user_id] = profile
    return profile


# PUBLIC_INTERFACE
@router.get("/profile/{user_id}", response_model=UserProfileSchema, summary="Get user profile")
def get_user_profile(user_id: str):
    """Retrieve a user profile by id (mocked)."""
    profile = MOCK_USER_DB.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# PUBLIC_INTERFACE
@router.patch("/profile/{user_id}", response_model=UserProfileSchema, summary="Update user profile")
def update_user_profile(user_id: str, request: UserProfileUpdateRequest):
    """Update an existing user profile (mocked)."""
    profile = MOCK_USER_DB.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    updated = profile.copy(update=request.dict(exclude_unset=True))
    MOCK_USER_DB[user_id] = updated
    return updated


# PUBLIC_INTERFACE
@router.post("/data", response_model=OnboardingDataSchema, summary="Save onboarding data")
def create_onboarding_data(request: OnboardingDataCreateRequest):
    """Save user's onboarding data (mocked)."""
    db_obj = OnboardingData(
        user_id=request.user_id,
        goals=request.goals,
        prior_experience=request.prior_experience,
        preferred_learning_style=request.preferred_learning_style,
        education_level=request.education_level,
        additional_info=request.additional_info,
    )
    MOCK_ONBOARDING_DB[request.user_id] = db_obj
    return db_obj


# PUBLIC_INTERFACE
@router.get("/data/{user_id}", response_model=OnboardingDataSchema, summary="Get onboarding data")
def get_onboarding_data(user_id: str):
    """Retrieve onboarding data for user (mocked)."""
    data = MOCK_ONBOARDING_DB.get(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Not found")
    return data
