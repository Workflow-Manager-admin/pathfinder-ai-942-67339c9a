from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.onboarding import router as onboarding_router
from .routes.learning_path import router as learning_path_router
from .routes.project_ideas import router as project_ideas_router
from .routes.dashboard import router as dashboard_router
from .routes.chat import router as chat_router

app = FastAPI(
    title="SkillBridge AI Backend",
    description=(
        "REST API for SkillBridge - AI-powered personalized learning and "
        "project ideas recommendation."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Onboarding", "description": "User onboarding and profile setup"},
        {"name": "Learning Paths", "description": "Personalized learning path management"},
        {"name": "Project Ideas", "description": "AI-suggested or generic project ideas"},
        {"name": "Dashboard", "description": "User dashboard and progress summary"},
        {"name": "Chat", "description": "Chatbot Q&A and support"},
    ],
)

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.onboarding import router as onboarding_router
from .routes.learning_path import router as learning_path_router
from .routes.project_ideas import router as project_ideas_router
from .routes.dashboard import router as dashboard_router
from .routes.chat import router as chat_router

# CORS origin setting for dev/demo, "*" for no cookies, or from environment
frontend_url = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app = FastAPI(
    title="SkillBridge AI Backend",
    description=(
        "REST API for SkillBridge - AI-powered personalized learning and "
        "project ideas recommendation."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Onboarding", "description": "User onboarding and profile setup"},
        {"name": "Learning Paths", "description": "Personalized learning path management"},
        {"name": "Project Ideas", "description": "AI-suggested or generic project ideas"},
        {"name": "Dashboard", "description": "User dashboard and progress summary"},
        {"name": "Chat", "description": "Chatbot Q&A and support"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(onboarding_router)
app.include_router(learning_path_router)
app.include_router(project_ideas_router)
app.include_router(dashboard_router)
app.include_router(chat_router)


@app.get("/")
def health_check():
    return {"message": "Healthy"}
