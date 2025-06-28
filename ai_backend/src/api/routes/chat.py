from fastapi import APIRouter
from typing import List
from ..schemas import (
    ChatMessageSchema,
    ChatMessageCreateRequest,
)
from ..services.chat import (
    generate_mock_chat_response,
    get_mock_chat_history,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# PUBLIC_INTERFACE
@router.get(
    "/history/{user_id}",
    response_model=List[ChatMessageSchema],
    summary="Get recent chat history",
)
def get_chat_history(user_id: str):
    """Return sample chat history for a user (mocked)."""
    return get_mock_chat_history(user_id)


# PUBLIC_INTERFACE
@router.post("/send", response_model=ChatMessageSchema, summary="Send message to assistant")
def send_message(request: ChatMessageCreateRequest):
    """Send a user message and get an assistant response (mock, non-AI)."""
    return generate_mock_chat_response(request)
