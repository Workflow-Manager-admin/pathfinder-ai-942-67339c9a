from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field


# SCHEMAS mirror the data models and serve as request/response formats for FastAPI endpoints.
# They are kept separate for extensibility, documentation, and security.
# (e.g., omit sensitive fields).


# PUBLIC_INTERFACE
class UserProfileSchema(BaseModel):
    """Schema for API representation of a user profile."""

    user_id: str = Field(
        ...,
        description="Unique id of the user"
    )
    name: str = Field(
        ...,
        description="Name of user"
    )
    email: str = Field(
        ...,
        description="User email"
    )
    bio: Optional[str] = Field(
        None,
        description="User biography"
    )
    avatar_url: Optional[str] = Field(
        None,
        description="URL for user avatar/profile picture"
    )
    interests: List[str] = Field(
        default_factory=list,
        description="List of user interests/skills"
    )
    role: Optional[str] = Field(
        None,
        description="Role (student, professional, etc.)"
    )
    created_at: Optional[datetime] = Field(
        None,
        description="Created timestamp"
    )


# PUBLIC_INTERFACE
class UserProfileCreateRequest(BaseModel):
    """Schema for creating a new user profile."""

    name: str = Field(
        ...,
        description="Name of user"
    )
    email: str = Field(
        ...,
        description="User email"
    )
    bio: Optional[str] = Field(
        None,
        description="User biography"
    )
    avatar_url: Optional[str] = Field(
        None,
        description="URL for user avatar"
    )
    interests: List[str] = Field(
        default_factory=list,
        description="List of user interests/skills"
    )
    role: Optional[str] = Field(
        None,
        description="Role"
    )


# PUBLIC_INTERFACE
class UserProfileUpdateRequest(BaseModel):
    """Schema for updating an existing user profile."""

    name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    interests: Optional[List[str]]
    role: Optional[str]


# PUBLIC_INTERFACE
class OnboardingDataSchema(BaseModel):
    """Schema for user onboarding data."""

    user_id: str
    goals: List[str]
    prior_experience: Optional[str]
    preferred_learning_style: Optional[str]
    education_level: Optional[str]
    additional_info: Optional[str]


# PUBLIC_INTERFACE
class OnboardingDataCreateRequest(BaseModel):
    """Schema for onboarding data creation."""

    user_id: str
    goals: List[str]
    prior_experience: Optional[str]
    preferred_learning_style: Optional[str]
    education_level: Optional[str]
    additional_info: Optional[str]


# PUBLIC_INTERFACE
class LearningPathItemSchema(BaseModel):
    """API representation of one step in a learning path."""

    id: str
    title: str
    description: Optional[str]
    resource_link: Optional[str]
    order: int


# PUBLIC_INTERFACE
class LearningPathSchema(BaseModel):
    """API schema for a personalized learning path."""

    path_id: str
    user_id: str
    name: str
    summary: Optional[str]
    items: List[LearningPathItemSchema]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# PUBLIC_INTERFACE
class LearningPathCreateRequest(BaseModel):
    """Request body for creating custom learning paths."""

    user_id: str
    name: str
    summary: Optional[str]
    items: List[LearningPathItemSchema]


# PUBLIC_INTERFACE
class ProjectIdeaSchema(BaseModel):
    """Schema for a project idea."""

    idea_id: str
    user_id: str
    title: str
    description: str
    technologies: List[str]
    difficulty: Optional[str]
    tags: List[str]
    created_at: Optional[datetime]


# PUBLIC_INTERFACE
class ProjectIdeaGenerateRequest(BaseModel):
    """Request for generating a new project idea."""

    user_id: str
    interests: List[str]
    difficulty: Optional[str]
    tags: Optional[List[str]]


# PUBLIC_INTERFACE
class ProjectIdeaCreateRequest(BaseModel):
    """Request for creating project idea manually."""

    user_id: str
    title: str
    description: str
    technologies: List[str]
    difficulty: Optional[str]
    tags: Optional[List[str]]


# PUBLIC_INTERFACE
class ChatMessageSchema(BaseModel):
    """Schema representing a chat or Q&A message."""

    message_id: str
    user_id: str
    sender: str
    content: str
    timestamp: datetime
    context_type: Optional[str]
    context_id: Optional[str]


# PUBLIC_INTERFACE
class ChatMessageCreateRequest(BaseModel):
    """Request for sending a chat message."""

    user_id: str
    sender: str
    content: str
    context_type: Optional[str]
    context_id: Optional[str]


# PUBLIC_INTERFACE
class UserProgressSchema(BaseModel):
    """Schema for reporting user progress on a path."""

    progress_id: str
    user_id: str
    path_id: str
    completed_items: List[str]
    in_progress_item: Optional[str]
    percent_complete: float
    last_updated: Optional[datetime]


# PUBLIC_INTERFACE
class UserProgressUpdateRequest(BaseModel):
    """Update request for marking user progress."""

    user_id: str
    path_id: str
    completed_items: Optional[List[str]]
    in_progress_item: Optional[str]
    percent_complete: Optional[float]
