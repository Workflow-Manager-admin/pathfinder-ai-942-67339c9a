from uuid import uuid4
from datetime import datetime
from typing import List
from ..models import ChatMessage
from ..schemas import ChatMessageCreateRequest


# PUBLIC_INTERFACE
def generate_mock_chat_response(request: ChatMessageCreateRequest) -> ChatMessage:
    """
    Generate a semi-intelligent, simulated "AI" response to a user chat message.

    This expands the prior stub. It detects question type, gives "AI-like" helpful
    suggestions, recommends learning path or project, and includes fallback rule-based
    replies—creating a more realistic Q&A experience.

    Easily upgradable to call a real LLM/OpenAI API in the future.

    Args:
        request (ChatMessageCreateRequest): The incoming user message.

    Returns:
        ChatMessage: Assistant's response.
    """
    user_text = request.content or ""
    lower_text = user_text.lower().strip()
    # Simple keyword/rule-based mock "AI" (could upgrade to OpenAI or transformers)
    if not user_text:
        mock_answer = (
            "Hi! Please type a question, for example: 'How do I start learning Python?'"
        )
    elif "python" in lower_text and "start" in lower_text:
        mock_answer = (
            "To get started with Python, begin with the 'Intro to Python Programming' "
            "module in your learning path. "
            "Would you like some recommended "
            "resources?"
        )
    elif "project" in lower_text and ("idea" in lower_text or "suggest" in lower_text):
        mock_answer = (
            "Looking for a project idea? How about building a weather app or a personal portfolio site? "
            "Let me know your interests or tech skills for tailored suggestions!"
        )
    elif "learning path" in lower_text or "module" in lower_text:
        mock_answer = (
            "Explore your personalized learning path to see modules that match your goals. "
            "Need advice on which topic to focus on next?"
        )
    elif "help" in lower_text:
        mock_answer = (
            "I'm here to help! Ask about learning topics, recommended courses, or project ideas. "
            "Example: 'Suggest a backend project' or 'What should I learn after Python basics?'"
        )
    elif "recommend" in lower_text or "suggest" in lower_text:
        mock_answer = (
            "Can you tell me your main interests or your preferred learning style? "
            "That will help me recommend courses or projects customized for you!"
        )
    elif "thank" in lower_text or "thanks" in lower_text:
        mock_answer = "You're welcome! Let me know if you have any more questions."
    elif lower_text.endswith("?"):
        mock_answer = (
            "That's a great question! Here's what I suggest: "
            "Try to search for resources in your learning path, or ask about a specific technology. "
            "If you need project ideas, just mention your skills!"
        )
    else:
        # Generic fallback: echo with encouragement, properly split long line
        mock_answer = (
            f"I received your message: '{user_text}'. "
            "If you want help with learning paths, programming, or new project "
            "ideas, please specify!"
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
