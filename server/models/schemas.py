from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str | None = None


class MemoryCreate(BaseModel):
    user_id: str
    layer: str = "co_built"
    category: str | None = None
    content: str


class MemoryUpdate(BaseModel):
    content: str | None = None
    category: str | None = None


class MemoryResponse(BaseModel):
    id: UUID
    user_id: str
    layer: str
    category: str | None
    content: str
    created_at: datetime
    updated_at: datetime


class IntimacyResponse(BaseModel):
    user_id: str
    score: int
    level: str
    next_milestone: int
