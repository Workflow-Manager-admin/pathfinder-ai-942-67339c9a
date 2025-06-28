from uuid import uuid4
from datetime import datetime
from typing import List
from ..models import ProjectIdea
from ..schemas import ProjectIdeaGenerateRequest


# PUBLIC_INTERFACE
def generate_mock_project_ideas(request: ProjectIdeaGenerateRequest) -> List[ProjectIdea]:
    """
    Generate a list of mock project ideas based on user interests, difficulty, and tags.
    Args:
        request (ProjectIdeaGenerateRequest): User's preferences.
    Returns:
        List[ProjectIdea]: List of project ideas.
    """
    now = datetime.utcnow()
    # This is mock logic. In real application this would be based on AI or rule-based system.
    sample_ideas = [
        ProjectIdea(
            idea_id=str(uuid4()),
            user_id=request.user_id,
            title="Personal Portfolio Website",
            description=(
                "Design and build a personal portfolio to showcase your projects and resume "
                "using React and modern CSS."
            ),
            technologies=["React", "CSS", "Vercel"],
            difficulty="Beginner",
            tags=["web", "portfolio", "frontend"],
            created_at=now,
        ),
        ProjectIdea(
            idea_id=str(uuid4()),
            user_id=request.user_id,
            title="Expense Tracker API",
            description=(
                "Develop an API for tracking expenses and generating monthly financial "
                "reports with Python's FastAPI."
            ),
            technologies=["FastAPI", "SQLite", "Python"],
            difficulty="Intermediate",
            tags=["api", "backend", "finance"],
            created_at=now,
        ),
        ProjectIdea(
            idea_id=str(uuid4()),
            user_id=request.user_id,
            title="Data Visualization Dashboard",
            description=(
                "Build a dashboard to visualize open datasets with interactive plots and filters."
            ),
            technologies=["Plotly", "Dash", "Pandas"],
            difficulty="Intermediate",
            tags=["data", "dashboard", "visualization"],
            created_at=now,
        ),
    ]
    # Optionally filter/mock-projects by tags, difficulty, or interests for demonstration
    filtered = [
        idea for idea in sample_ideas
        if (not request.difficulty or idea.difficulty == request.difficulty)
        and (not request.tags or any(tag in idea.tags for tag in (request.tags or [])))
        and (
            not request.interests
            or any(skill in idea.tags + idea.technologies for skill in request.interests)
        )
    ]
    return filtered or sample_ideas  # fallback to all if no match


# PUBLIC_INTERFACE
def get_generic_project_ideas() -> List[ProjectIdea]:
    """
    Return a generic non-personalized list of project ideas.
    """
    now = datetime.utcnow()
    return [
        ProjectIdea(
            idea_id=str(uuid4()),
            user_id="",
            title="Weather App",
            description=(
                "Create a web/mobile app to fetch and display live weather data "
                "for chosen locations."
            ),
            technologies=["Python", "FastAPI", "React"],
            difficulty="Beginner",
            tags=["web", "api", "weather"],
            created_at=now,
        ),
        ProjectIdea(
            idea_id=str(uuid4()),
            user_id="",
            title="Chatbot for FAQs",
            description=(
                "Develop a simple chatbot that answers common questions "
                "about a topic of your choice."
            ),
            technologies=["Python", "NLP", "FastAPI"],
            difficulty="Intermediate",
            tags=["chatbot", "nlp", "ai"],
            created_at=now,
        ),
    ]
