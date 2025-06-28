from fastapi import APIRouter, HTTPException
from ..schemas import (
    OnboardingDataSchema,
    OnboardingDataCreateRequest,
    UserProfileSchema,
    UserProfileCreateRequest,
    UserProfileUpdateRequest,
)
from ..models import OnboardingData, UserProfile
from ..storage import (
    save_user_profile,
    get_user_profile as storage_get_user_profile,
    update_user_profile as storage_update_user_profile,
    save_onboarding_data,
    get_onboarding_data as storage_get_onboarding_data
)
from uuid import uuid4
from datetime import datetime


router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"],
)


# PUBLIC_INTERFACE
@router.post("/profile", response_model=UserProfileSchema, summary="Create user profile")
def create_user_profile(request: UserProfileCreateRequest):
    """Create a new user profile and persist it."""
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
    save_user_profile(profile.model_dump())
    return profile


# PUBLIC_INTERFACE
@router.get("/profile/{user_id}", response_model=UserProfileSchema, summary="Get user profile")
def get_profile(user_id: str):
    """Retrieve a user profile by id."""
    doc = storage_get_user_profile(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfile(**doc)


# PUBLIC_INTERFACE
@router.patch("/profile/{user_id}", response_model=UserProfileSchema, summary="Update user profile")
def update_profile(user_id: str, request: UserProfileUpdateRequest):
    """Update an existing user profile."""
    data = request.dict(exclude_unset=True)
    updated = storage_update_user_profile(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfile(**updated)


# PUBLIC_INTERFACE
@router.post("/data", response_model=OnboardingDataSchema, summary="Save onboarding data")
def create_onboarding_data(request: OnboardingDataCreateRequest):
    """Save user's onboarding data."""
    db_obj = OnboardingData(
        user_id=request.user_id,
        goals=request.goals,
        prior_experience=request.prior_experience,
        preferred_learning_style=request.preferred_learning_style,
        education_level=request.education_level,
        additional_info=request.additional_info,
    )
    save_onboarding_data(request.user_id, db_obj.model_dump())
    return db_obj


# PUBLIC_INTERFACE
@router.get("/data/{user_id}", response_model=OnboardingDataSchema, summary="Get onboarding data")
def get_onboarding_data_route(user_id: str):
    """Retrieve onboarding data for user."""
    doc = storage_get_onboarding_data(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return OnboardingData(**doc)
