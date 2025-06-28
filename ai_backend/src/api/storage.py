import json
import os
from threading import Lock
from typing import Any, Dict, List, Optional

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(STORAGE_DIR, exist_ok=True)

_LOCKS = {
    "user_profiles": Lock(),
    "onboarding_data": Lock(),
    "learning_paths": Lock(),
    "project_ideas": Lock(),
    "user_progress": Lock(),
    "chat_messages": Lock(),
}

_FILES = {
    "user_profiles": os.path.join(STORAGE_DIR, "user_profiles.json"),
    "onboarding_data": os.path.join(STORAGE_DIR, "onboarding_data.json"),
    "learning_paths": os.path.join(STORAGE_DIR, "learning_paths.json"),
    "project_ideas": os.path.join(STORAGE_DIR, "project_ideas.json"),
    "user_progress": os.path.join(STORAGE_DIR, "user_progress.json"),
    "chat_messages": os.path.join(STORAGE_DIR, "chat_messages.json"),
}


def _read_json(file_key: str) -> Dict[str, Any]:
    fname = _FILES[file_key]
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def _write_json(file_key: str, data: Dict[str, Any]):
    fname = _FILES[file_key]
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# PUBLIC_INTERFACE
def save_user_profile(profile: dict):
    """Save or update a user profile dict by user_id key."""
    k = "user_profiles"
    with _LOCKS[k]:
        db = _read_json(k)
        db[profile["user_id"]] = profile
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_user_profile(user_id: str) -> Optional[dict]:
    """Fetch a user profile."""
    k = "user_profiles"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(user_id)


# PUBLIC_INTERFACE
def update_user_profile(user_id: str, updates: dict) -> Optional[dict]:
    """Update user profile fields."""
    k = "user_profiles"
    with _LOCKS[k]:
        db = _read_json(k)
        prof = db.get(user_id)
        if prof is None:
            return None
        prof.update(updates)
        db[user_id] = prof
        _write_json(k, db)
        return prof


# PUBLIC_INTERFACE
def save_onboarding_data(user_id: str, data: dict):
    """Save or update onboarding data for a user."""
    k = "onboarding_data"
    with _LOCKS[k]:
        db = _read_json(k)
        db[user_id] = data
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_onboarding_data(user_id: str) -> Optional[dict]:
    """Get onboarding data for a user."""
    k = "onboarding_data"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(user_id)


# PUBLIC_INTERFACE
def save_learning_path(path: dict):
    """Save or update a personalized learning path by path_id."""
    k = "learning_paths"
    with _LOCKS[k]:
        db = _read_json(k)
        db[path["path_id"]] = path
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_learning_paths_for_user(user_id: str) -> List[dict]:
    """Get all learning paths for a user."""
    k = "learning_paths"
    with _LOCKS[k]:
        db = _read_json(k)
        return [v for v in db.values() if v.get("user_id") == user_id]


# PUBLIC_INTERFACE
def get_learning_path(path_id: str) -> Optional[dict]:
    """Retrieve learning path by its id."""
    k = "learning_paths"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(path_id)


# PUBLIC_INTERFACE
def save_project_idea(idea: dict):
    """Store a project idea."""
    k = "project_ideas"
    with _LOCKS[k]:
        db = _read_json(k)
        db[idea["idea_id"]] = idea
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_project_ideas_for_user(user_id: str) -> List[dict]:
    """Get project ideas for a given user, or all, if user_id is ''."""
    k = "project_ideas"
    with _LOCKS[k]:
        db = _read_json(k)
        if not user_id:
            return [v for v in db.values() if not v.get("user_id")]
        return [v for v in db.values() if v.get("user_id") == user_id]


# PUBLIC_INTERFACE
def get_project_idea(idea_id: str) -> Optional[dict]:
    """Get a project idea by id."""
    k = "project_ideas"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(idea_id)


# PUBLIC_INTERFACE
def save_user_progress(progress: dict):
    """Store progress for a learning path (one per user+path_id)."""
    k = "user_progress"
    key = f"{progress['user_id']}|{progress['path_id']}"
    with _LOCKS[k]:
        db = _read_json(k)
        db[key] = progress
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_user_progress(user_id: str, path_id: str) -> Optional[dict]:
    """Get specific user progress by user + path id."""
    k = "user_progress"
    key = f"{user_id}|{path_id}"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(key)


# PUBLIC_INTERFACE
def save_chat_message(msg: dict):
    """Append a chat message for a user+context."""
    k = "chat_messages"
    uid = msg["user_id"]
    with _LOCKS[k]:
        db = _read_json(k)
        if uid not in db:
            db[uid] = []
        db[uid].append(msg)
        _write_json(k, db)


# PUBLIC_INTERFACE
def get_chat_history(user_id: str) -> List[dict]:
    """Return all chat messages for user."""
    k = "chat_messages"
    with _LOCKS[k]:
        db = _read_json(k)
        return db.get(user_id, [])
