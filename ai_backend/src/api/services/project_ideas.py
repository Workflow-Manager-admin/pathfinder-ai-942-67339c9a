from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from ..models import ProjectIdea
from ..schemas import ProjectIdeaGenerateRequest
from ..storage import get_user_profile, get_onboarding_data

# Sample rule-based idea definitions. Each template contains a matcher
# for interests/goals, base idea definition, and dynamic elements.
_SAMPLE_TEMPLATES = [
    {
        "matcher": lambda interests, goals: (
            "python" in [i.lower() for i in interests]
        ),
        "title": "Python Automation Tool",
        "description": (
            "Automate a repetitive task (e.g., file renaming, CSV processing) "
            "with a Python script. Useful for those new to scripting."
        ),
        "technologies": ["Python"],
        "difficulty": "Beginner",
        "tags": ["python", "automation", "script"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "web" in [i.lower() for i in interests]
                or "frontend" in [i.lower() for i in interests]
            )
        ),
        "title": "Personal Portfolio Website",
        "description": (
            "Design and build a personal portfolio to showcase your projects and resume "
            "using React and modern CSS."
        ),
        "technologies": ["React", "CSS", "Vercel"],
        "difficulty": "Beginner",
        "tags": ["web", "portfolio", "frontend"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "api" in [i.lower() for i in interests]
                or "backend" in [i.lower() for i in interests]
            )
        ),
        "title": "Expense Tracker API",
        "description": (
            "Develop a REST API for tracking expenses and generating monthly financial reports. "
            "Learn CRUD, authentication, and data handling."
        ),
        "technologies": ["FastAPI", "SQLite", "Python"],
        "difficulty": "Intermediate",
        "tags": ["api", "backend", "finance"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "data science" in [i.lower() for i in interests]
                or "data viz" in [i.lower() for i in interests]
                or "visualization" in [i.lower() for i in interests]
            )
        ),
        "title": "Data Visualization Dashboard",
        "description": (
            "Build an interactive dashboard to visualize open datasets with charts, "
            "filters, and modern web UI."
        ),
        "technologies": ["Plotly", "Dash", "Pandas"],
        "difficulty": "Intermediate",
        "tags": ["data", "dashboard", "visualization"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "nlp" in [i.lower() for i in interests]
                or "ai" in [i.lower() for i in interests]
                or "chatbot" in [i.lower() for i in interests]
                or "faq bot" in goals
            )
        ),
        "title": "Chatbot for FAQs",
        "description": (
            "Develop a simple chatbot that answers common questions "
            "using rule-based logic or NLP for frequently asked topics."
        ),
        "technologies": ["Python", "NLP", "FastAPI"],
        "difficulty": "Intermediate",
        "tags": ["chatbot", "nlp", "ai"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "mobile" in [i.lower() for i in interests]
            )
        ),
        "title": "Simple Mobile To-Do App",
        "description": (
            "Create a minimal to-do list app for mobile using React Native or Flutter, "
            "with local storage and task reminders."
        ),
        "technologies": ["React Native", "Flutter"],
        "difficulty": "Beginner",
        "tags": ["mobile", "app", "todo"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "finance" in [i.lower() for i in interests]
                or "budget" in goals
            )
        ),
        "title": "Personal Finance Dashboard",
        "description": (
            "Develop a dashboard to track spending, set savings goals, "
            "and visualize finances. Integrate charts and local CSV upload."
        ),
        "technologies": ["Python", "Dash", "Plotly"],
        "difficulty": "Intermediate",
        "tags": ["finance", "dashboard", "data viz"],
    },
    {
        "matcher": (
            lambda interests, goals: (
                "education" in goals or "teach" in goals
            )
        ),
        "title": "Interactive Learning App",
        "description": (
            "Build an educational app to quiz users on chosen topics. "
            "Includes scoring, review, and user-added questions."
        ),
        "technologies": ["React", "Node.js", "MongoDB"],
        "difficulty": "Intermediate",
        "tags": ["education", "quiz", "web app"],
    },
]

# Fallback pool if nothing matches
_GENERIC_IDEAS = [
    {
        "title": "Weather App",
        "description": (
            "Create a web/mobile app to fetch and display live weather data "
            "for chosen locations."
        ),
        "technologies": ["Python", "FastAPI", "React"],
        "difficulty": "Beginner",
        "tags": ["web", "api", "weather"],
    },
    {
        "title": "Blog Platform",
        "description": (
            "Develop a basic blogging platform where users can post, edit, "
            "and comment on articles."
        ),
        "technologies": ["Django", "SQLite", "Bootstrap"],
        "difficulty": "Intermediate",
        "tags": ["web", "blog", "backend"],
    },
]


def _collect_user_context(user_id: str, request: ProjectIdeaGenerateRequest):
    # Try to fetch onboarding/profile for richer personalization.
    # Use request-provided interests/tags as fallback if storage not found.
    profile: Optional[dict] = get_user_profile(user_id) or {}
    onboarding: Optional[dict] = get_onboarding_data(user_id) or {}

    # Prefer richer data for rule-based matching. Lowercased.
    interests = (
        (request.interests or []) +
        profile.get("interests", [])
    )
    goals = onboarding.get("goals", [])

    # Deduplicate and lowercase for matching in rules.
    interests_out = list(
        set([i.lower() for i in interests if isinstance(i, str)])
    )
    goals_out = list(
        set([g.lower() for g in goals if isinstance(g, str)])
    )
    return interests_out, goals_out


# PUBLIC_INTERFACE
def generate_mock_project_ideas(request: ProjectIdeaGenerateRequest) -> List[ProjectIdea]:
    """
    Generate a list of rule-based, profile-personalized project ideas.
    Uses onboarding/profile data and preferences for meaningful recommendations.

    Args:
        request (ProjectIdeaGenerateRequest): User's preferences.
    Returns:
        List[ProjectIdea]: List of project ideas.
    """
    now = datetime.utcnow()
    # Gather interests/goals using both API input and user profile + onboarding
    interests, goals = _collect_user_context(request.user_id, request)
    provided_tags = [t.lower() for t in (request.tags or [])]

    # Find ideas based on rule-matching: interest, goal, difficulty, or tag.
    personalized = []
    used_titles = set()
    for template in _SAMPLE_TEMPLATES:
        # Rule: matches at least one of the user's interests/goals using template's matcher.
        if template["matcher"](interests, goals):
            # Respect explicit difficulty or tags if specified.
            if (
                request.difficulty and template.get("difficulty") and
                template["difficulty"].lower() != request.difficulty.lower()
            ):
                continue
            if (
                provided_tags and
                not any(tag in template.get("tags", []) for tag in provided_tags)
            ):
                continue
            personalized.append(ProjectIdea(
                idea_id=str(uuid4()),
                user_id=request.user_id,
                title=template["title"],
                description=template["description"],
                technologies=template["technologies"],
                difficulty=template["difficulty"],
                tags=template["tags"],
                created_at=now,
            ))
            used_titles.add(template["title"])

    # If not enough results, pad with generic ideas
    while (
        len(personalized) < 3
        and
        len(personalized) < len(_SAMPLE_TEMPLATES) + len(_GENERIC_IDEAS)
    ):
        for fallback in _GENERIC_IDEAS:
            if fallback["title"] in used_titles:
                continue
            if (
                request.difficulty
                and
                fallback.get("difficulty")
                and
                fallback["difficulty"].lower() != request.difficulty.lower()
            ):
                continue
            if (
                provided_tags
                and
                not any(
                    tag in fallback.get("tags", [])
                    for tag in provided_tags
                )
            ):
                continue
            personalized.append(ProjectIdea(
                idea_id=str(uuid4()),
                user_id=request.user_id,
                title=fallback["title"],
                description=fallback["description"],
                technologies=fallback["technologies"],
                difficulty=fallback["difficulty"],
                tags=fallback["tags"],
                created_at=now,
            ))
            used_titles.add(fallback["title"])
            if len(personalized) >= 3:
                break
        else:
            break

    # If still nothing, fallback to all generics (ignore personalization)
    if not personalized:
        personalized = [
            ProjectIdea(
                idea_id=str(uuid4()),
                user_id=request.user_id,
                title=idea["title"],
                description=idea["description"],
                technologies=idea["technologies"],
                difficulty=idea["difficulty"],
                tags=idea["tags"],
                created_at=now,
            )
            for idea in _GENERIC_IDEAS
        ]
    return personalized


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
            title=idea["title"],
            description=idea["description"],
            technologies=idea["technologies"],
            difficulty=idea["difficulty"],
            tags=idea["tags"],
            created_at=now,
        )
        for idea in _GENERIC_IDEAS
    ]
