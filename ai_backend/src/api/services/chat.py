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
    # SYSTEM PROMPT (optional, configure if needed)
    system_instructions = (
        "You are SkillBridge AI—an empathetic, knowledgeable assistant that gives clear, "
        "practical guidance on tech learning, careers, and project ideas. Tailor suggestions to "
        "the user's level. Do not assume context not provided."
    )
    # Prepare request with optional system prompt and stateless chat for now.
    data = {
        "message": user_text,
        "model": COHERE_MODEL,
        "preamble": system_instructions,
        # "temperature": 0.6,  # Optionally tune temperature
        # Optionally, add "chat_history" (list of {role,msg}) for context
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
            # Handle bad responses robustly even if not JSON
            try:
                resp_json = response.json()
                # Cohere sometimes uses "message", sometimes "error", nested vals
                detail = (
                    resp_json.get("message")
                    or resp_json.get("error")
                    or resp_json.get("error_message")
                    or response.text
                )
            except Exception:
                detail = response.text
            error_message = (
                "Sorry, I couldn't process your message due to an API error: "
                f"{detail}"
            )
        else:
            resp_json = response.json()
            # Cohere v1 returns "text" (most common), "reply" (sometimes), or "generations"
            ai_reply = resp_json.get("text") or resp_json.get("reply")
            # Fallback: check for "generations" (OpenAI-style; Cohere sometimes adapts)
            if not ai_reply and "generations" in resp_json:
                gens = resp_json.get("generations")
                if isinstance(gens, list) and gens:
                    ai_reply = gens[0].get("text")
            if not ai_reply:
                error_message = (
                    "Received empty or unrecognized AI response from Cohere. "
                    "Please try again later."
                )
    except httpx.RequestError:
        error_message = (
            "There was a network error reaching the AI service. Please try again."
        )
    except Exception as ex:
        error_message = (
            f"Something went wrong when generating your answer "
            f"({type(ex).__name__}): {ex}"
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
