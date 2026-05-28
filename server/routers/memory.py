from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.models.schemas import MemoryCreate, MemoryResponse, MemoryUpdate
from server.services import memory_service

router = APIRouter(prefix="/api/memories", tags=["memory"])


@router.get("/{user_id}", response_model=list[MemoryResponse])
async def list_memories(
    user_id: str,
    layer: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    memories = await memory_service.get_memories(db, user_id, layer)
    return memories


@router.post("", response_model=MemoryResponse, status_code=201)
async def create_memory(
    body: MemoryCreate,
    db: AsyncSession = Depends(get_db),
):
    memory = await memory_service.add_memory(
        db,
        user_id=body.user_id,
        layer=body.layer,
        content=body.content,
        category=body.category,
    )
    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: UUID,
    body: MemoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    memory = await memory_service.update_memory(
        db,
        memory_id=memory_id,
        content=body.content,
        category=body.category,
    )
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.delete("/{memory_id}", status_code=204)
async def delete_memory(
    memory_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    deleted = await memory_service.delete_memory(db, memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")


@router.get("/{user_id}/search")
async def search_memories(
    user_id: str,
    q: str,
    top_k: int = 5,
    db: AsyncSession = Depends(get_db),
):
    memories = await memory_service.search_memories(db, user_id, q, top_k)
    return memories
