import json
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.db_models import Memory
from server.services.llm import chat, get_embedding
from server.services.prompt_builder import MEMORY_EXTRACTION_PROMPT


async def add_memory(
    db: AsyncSession,
    user_id: str,
    layer: str,
    content: str,
    category: str | None = None,
) -> Memory:
    embedding = await get_embedding(content)
    memory = Memory(
        user_id=user_id,
        layer=layer,
        category=category,
        content=content,
        embedding=embedding,
    )
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


async def get_memories(
    db: AsyncSession,
    user_id: str,
    layer: str | None = None,
) -> list[Memory]:
    stmt = select(Memory).where(Memory.user_id == user_id)
    if layer:
        stmt = stmt.where(Memory.layer == layer)
    stmt = stmt.order_by(Memory.updated_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def search_memories(
    db: AsyncSession,
    user_id: str,
    query: str,
    top_k: int = 5,
) -> list[Memory]:
    query_embedding = await get_embedding(query)
    if query_embedding is None:
        stmt = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .where(Memory.content.ilike(f"%{query}%"))
            .order_by(Memory.updated_at.desc())
            .limit(top_k)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
    stmt = (
        select(Memory)
        .where(Memory.user_id == user_id)
        .where(Memory.embedding.isnot(None))
        .order_by(Memory.embedding.cosine_distance(query_embedding))
        .limit(top_k)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_memory(
    db: AsyncSession,
    memory_id: UUID,
    content: str | None = None,
    category: str | None = None,
) -> Memory | None:
    result = await db.execute(select(Memory).where(Memory.id == memory_id))
    memory = result.scalar_one_or_none()
    if not memory:
        return None

    if content is not None:
        memory.content = content
        embedding = await get_embedding(content)
        if embedding is not None:
            memory.embedding = embedding
    if category is not None:
        memory.category = category
    memory.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(memory)
    return memory


async def delete_memory(db: AsyncSession, memory_id: UUID) -> bool:
    result = await db.execute(delete(Memory).where(Memory.id == memory_id))
    await db.commit()
    return result.rowcount > 0


async def extract_memories_from_chat(
    db: AsyncSession,
    user_id: str,
    conversation_text: str,
) -> list[Memory]:
    prompt = MEMORY_EXTRACTION_PROMPT.format(conversation=conversation_text)
    response = await chat([{"role": "user", "content": prompt}])

    try:
        extracted = json.loads(response)
    except json.JSONDecodeError:
        return []

    new_memories = []
    for item in extracted:
        if "content" in item:
            memory = await add_memory(
                db,
                user_id=user_id,
                layer="co_built",
                content=item["content"],
                category=item.get("category"),
            )
            new_memories.append(memory)
    return new_memories
