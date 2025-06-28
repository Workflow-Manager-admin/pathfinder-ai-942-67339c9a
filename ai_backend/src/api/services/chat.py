from uuid import uuid4
from datetime import datetime
from typing import List
from ..models import ChatMessage
from ..schemas import ChatMessageCreateRequest


# PUBLIC_INTERFACE
def generate_mock_chat_response(request: ChatMessageCreateRequest) -> ChatMessage:
    """
    Generate a mock/AI-stub response to a user chat message.
    For MVP, this rephrases the user input as if answered by 'assistant'.

    Args:
        request (ChatMessageCreateRequest): The incoming user message.
    Returns:
        ChatMessage: Assistant's response.
    """
    mock_answer = (
        f"I see you're asking: '{request.content}'. "
        "For more details, check your learning path or ask about a specific course or topic!"
    )
    answer = ChatMessage(
        message_id=str(uuid4()),
        user_id=request.user_id,
        sender="assistant",
        content=mock_answer,
        timestamp=datetime.utcnow(),
        context_type=request.context_type,
        context_id=request.context_id
    )
    return answer


# PUBLIC_INTERFACE
def get_mock_chat_history(
    user_id: str,
    context_type: str = None,
    context_id: str = None
) -> List[ChatMessage]:
    """
    Return a sample chat/Q&A history for a user.
    """
    now = datetime.utcnow()
    return [
        ChatMessage(
            message_id=str(uuid4()),
            user_id=user_id,
            sender="user",
            content="How do I get started with Python?",
            timestamp=now,
            context_type=context_type,
            context_id=context_id,
        ),
        ChatMessage(
            message_id=str(uuid4()),
            user_id=user_id,
            sender="assistant",
            content=(
                "Check out the 'Intro to Python Programming' module in your learning path! "
                "Would you like more beginner resources?"
            ),
            timestamp=now,
            context_type=context_type,
            context_id=context_id,
        ),
    ]
