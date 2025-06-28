import httpx
from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from ..models import ChatMessage
from ..schemas import ChatMessageCreateRequest


COHERE_API_URL = "https://api.cohere.ai/v1/chat"
COHERE_API_KEY = "xyV9r163fmM8ieMhIFAUbmymr6DakgKJ8wj520lv"
COHERE_MODEL = "command-r-plus"  # Or adjust to "command" or most suitable as per use/tier

# Used for timeout on Cohere request
_DEFAULT_TIMEOUT = 10.0


# PUBLIC_INTERFACE
def generate_mock_chat_response(request: ChatMessageCreateRequest) -> ChatMessage:
    """
    Generate a real AI chat response by sending the request to Cohere's /chat API endpoint.

    Args:
        request (ChatMessageCreateRequest): The incoming user message.

    Returns:
        ChatMessage: Assistant's response.
    """
    user_text = request.content or ""
    # Prepare message history (optional): not implemented, for now send stateless request.
    # To use previous context, you may wish to collect chat history from storage here and pass as "chat_history"
    data = {
        "message": user_text,
        "model": COHERE_MODEL,
        # Optionally, system prompt, chat_history, temperature, etc.
    }
    auth_header = "Bearer " + COHERE_API_KEY
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    ai_reply = None
    error_message = None
    try:
        with httpx.Client(timeout=_DEFAULT_TIMEOUT) as client:
            response = client.post(COHERE_API_URL, headers=headers, json=data)
        if response.status_code != 200:
            # Possible errors: Invalid API key (401), bad input, rate limit, network etc.
            detail = response.json().get("message") or response.text
            error_message = (
                "Sorry, I couldn't process your message due to an API error: "
                f"{detail}"
            )
        else:
            resp_json = response.json()
            # Cohere returns "text" or "reply" key, depending on version
            ai_reply = resp_json.get("text") or resp_json.get("reply")
            if not ai_reply:
                error_message = "Received empty AI response. Please try again."
    except httpx.RequestError:
        error_message = (
            "There was a network error reaching the AI service. Please try again."
        )
    except Exception:
        error_message = (
            "Something went wrong when generating your answer. Please try again."
        )
    answer = ChatMessage(
        message_id=str(uuid4()),
        user_id=request.user_id,
        sender="assistant",
        content=ai_reply if ai_reply else error_message,
        timestamp=datetime.utcnow(),
        context_type=request.context_type,
        context_id=request.context_id,
    )
    return answer


# PUBLIC_INTERFACE
def get_mock_chat_history(
    user_id: str,
    context_type: Optional[str] = None,
    context_id: Optional[str] = None
) -> List[ChatMessage]:
    """
    Return a sample chat/Q&A history for a user.
    (This does not fetch from Cohere, for now returns a fixed example.)
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
