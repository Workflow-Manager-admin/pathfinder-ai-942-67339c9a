from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class UserProfile(BaseModel):
    """User profile data model."""

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
        description="Role, e.g., student, professional"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )


# PUBLIC_INTERFACE
class OnboardingData(BaseModel):
    """User onboarding data model."""

    user_id: str = Field(
        ...,
        description="Unique id of the user"
    )
    goals: List[str] = Field(
        default_factory=list,
        description="Learning or career goals"
    )
    prior_experience: Optional[str] = Field(
        None,
        description="Prior experience in related fields"
    )
    preferred_learning_style: Optional[str] = Field(
        None,
        description="Preferred learning style (e.g., video, text, interactive)"
    )
    education_level: Optional[str] = Field(
        None,
        description="Education level"
    )
    additional_info: Optional[str] = Field(
        None,
        description="Any additional onboarding info"
    )


# PUBLIC_INTERFACE
class LearningPathItem(BaseModel):
    """Individual step or course in a learning path."""

    id: str = Field(
        ...,
        description="Unique id for the learning path item"
    )
    title: str = Field(
        ...,
        description="Title or name of the learning path item"
    )
    description: Optional[str] = Field(
        None,
        description="Summary or details of this step"
    )
    resource_link: Optional[str] = Field(
        None,
        description="URL to the resource for this item"
    )
    order: int = Field(
        ...,
        description="Order of this item in the learning path"
    )


# PUBLIC_INTERFACE
class LearningPath(BaseModel):
    """User's personalized learning path."""

    path_id: str = Field(
        ...,
        description="Unique id for the learning path"
    )
    user_id: str = Field(
        ...,
        description="Id of the user this path is for (or None for generic)"
    )
    name: str = Field(
        ...,
        description="Name/title of the learning path"
    )
    summary: Optional[str] = Field(
        None,
        description="Short summary or objective"
    )
    items: List[LearningPathItem] = Field(
        default_factory=list,
        description="Ordered list of learning modules/steps"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )


# PUBLIC_INTERFACE
class ProjectIdea(BaseModel):
    """AI-generated or recommended project idea."""

    idea_id: str = Field(
        ...,
        description="Project idea unique id"
    )
    user_id: str = Field(
        ...,
        description="User id if personalized, else None for generic"
    )
    title: str = Field(
        ...,
        description="Project idea title"
    )
    description: str = Field(
        ...,
        description="Project summary/requirements"
    )
    technologies: List[str] = Field(
        default_factory=list,
        description="Tech stack or tools recommended"
    )
    difficulty: Optional[str] = Field(
        None,
        description="Suggested difficulty level"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Related skills/topics"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )


# PUBLIC_INTERFACE
class ChatMessage(BaseModel):
    """Record of a chat or Q&A exchange."""

    message_id: str = Field(
        ...,
        description="Message unique id"
    )
    user_id: str = Field(
        ...,
        description="User id"
    )
    sender: str = Field(
        ...,
        description="Who sent the message: user or assistant"
    )
    content: str = Field(
        ...,
        description="Message content"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )
    context_type: Optional[str] = Field(
        None,
        description="Optional context (e.g., learning_path, onboarding)"
    )
    context_id: Optional[str] = Field(
        None,
        description="ID related to the context, if any"
    )


# PUBLIC_INTERFACE
class UserProgress(BaseModel):
    """Progress of a user within a learning path or modules."""

    progress_id: str = Field(
        ...,
        description="Unique id for this progress record"
    )
    user_id: str = Field(
        ...,
        description="User id"
    )
    path_id: str = Field(
        ...,
        description="Learning path id"
    )
    completed_items: List[str] = Field(
        default_factory=list,
        description="List of ids of completed path items"
    )
    in_progress_item: Optional[str] = Field(
        None,
        description="Currently active item id, if any"
    )
    percent_complete: float = Field(
        ...,
        description="Completion percent (0-100)"
    )
    last_updated: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )
