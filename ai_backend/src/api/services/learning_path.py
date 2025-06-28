from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from ..models import LearningPath, LearningPathItem
from ..schemas import LearningPathCreateRequest


# PUBLIC_INTERFACE
def generate_mock_learning_path(
    user_id: str,
    name: Optional[str] = None,
    summary: Optional[str] = None
) -> LearningPath:
    """
    Generate a mock personalized learning path for a user.

    Args:
        user_id (str): Unique user id for whom the path is generated.
        name (str, optional): Name/title of the learning path.
        summary (str, optional): Brief summary of the learning objective.
    Returns:
        LearningPath: A mocked up example of a learning path.
    """
    path_id = str(uuid4())
    now = datetime.utcnow()
    mock_items = [
        LearningPathItem(
            id=str(uuid4()),
            title="Intro to Python Programming",
            description=(
                "Foundational Python syntax, variables, loops, and functions."
            ),
            resource_link="https://realpython.com/start-here/",
            order=1,
        ),
        LearningPathItem(
            id=str(uuid4()),
            title="Python Data Structures",
            description=(
                "Lists, dicts, sets, tuples and their use in everyday Python."
            ),
            resource_link=(
                "https://docs.python.org/3/tutorial/datastructures.html"
            ),
            order=2,
        ),
        LearningPathItem(
            id=str(uuid4()),
            title="APIs and Web Development Basics",
            description=(
                "Understand REST concepts, HTTP basics, and building APIs using FastAPI."
            ),
            resource_link="https://fastapi.tiangolo.com/tutorial/",
            order=3,
        ),
        LearningPathItem(
            id=str(uuid4()),
            title="Sample Project: Build a REST API",
            description=(
                "Combine your skills to build a simple CRUD API for a todo app."
            ),
            resource_link="https://github.com/tiangolo/full-stack-fastapi-postgresql",
            order=4,
        ),
    ]
    return LearningPath(
        path_id=path_id,
        user_id=user_id,
        name=name or "Python Developer Starter Path",
        summary=(
            summary
            or "Step-by-step beginner learning journey to understand Python and build your first API."
        ),
        items=mock_items,
        created_at=now,
        updated_at=now
    )


# PUBLIC_INTERFACE
def create_learning_path(request: LearningPathCreateRequest) -> LearningPath:
    """
    Create a learning path from the given request, simulating storage.
    (In real code, store in DB; now just constructs and returns.)
    """
    now = datetime.utcnow()
    new_items = [
        LearningPathItem(
            id=item.id or str(uuid4()),
            title=item.title,
            description=item.description,
            resource_link=item.resource_link,
            order=item.order,
        )
        for item in request.items
    ]
    return LearningPath(
        path_id=str(uuid4()),
        user_id=request.user_id,
        name=request.name,
        summary=request.summary,
        items=new_items,
        created_at=now,
        updated_at=now,
    )


# PUBLIC_INTERFACE
def get_mock_learning_paths_for_user(user_id: str) -> List[LearningPath]:
    """
    Return a list of sample (mock) learning paths for a user.
    """
    return [generate_mock_learning_path(user_id)]
