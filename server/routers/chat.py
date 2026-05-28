import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.auth import verify_token
from server.database import get_db
from server.models.db_models import Conversation, Memory
from server.models.schemas import ChatRequest
from server.services.llm import stream_chat
from server.services.prompt_builder import build_system_prompt

router = APIRouter(prefix="/api", tags=["chat"], dependencies=[Depends(verify_token)])

HISTORY_LIMIT = 20
SESSION_EXPIRE_DAYS = 7


@router.post("/chat")
async def chat_endpoint(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    session_id = req.session_id or str(uuid.uuid4())

    history_result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == req.user_id, Conversation.session_id == session_id)
        .order_by(Conversation.created_at.desc())
        .limit(HISTORY_LIMIT)
    )
    history_rows = list(reversed(history_result.scalars().all()))

    mem_result = await db.execute(
        select(Memory)
        .where(Memory.user_id == req.user_id)
        .order_by(Memory.updated_at.desc())
        .limit(20)
    )
    memories = [
        {"layer": m.layer, "content": m.content, "category": m.category}
        for m in mem_result.scalars().all()
    ]

    from server.services.intimacy_service import compute_score
    score = await compute_score(db, req.user_id)

    system_prompt = build_system_prompt(memories=memories, intimacy_score=score)
    messages = [{"role": "system", "content": system_prompt}]
    for row in history_rows:
        messages.append({"role": row.role, "content": row.content})
    messages.append({"role": "user", "content": req.message})

    db.add(Conversation(
        user_id=req.user_id,
        session_id=session_id,
        role="user",
        content=req.message,
    ))
    await db.commit()

    async def generate():
        full_response = []
        async for token in stream_chat(messages):
            full_response.append(token)
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

        assistant_content = "".join(full_response)
        db.add(Conversation(
            user_id=req.user_id,
            session_id=session_id,
            role="assistant",
            content=assistant_content,
        ))

        from server.services.intimacy_service import record_event
        from server.services.memory_service import extract_memories_from_chat
        await record_event(db, req.user_id, "chat")
        await db.commit()

        conversation_text = f"用户: {req.message}\n助手: {assistant_content}"
        try:
            await extract_memories_from_chat(db, req.user_id, conversation_text)
        except Exception:
            pass

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/conversations/{user_id}")
async def get_conversations(
    user_id: str,
    session_id: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Conversation).where(Conversation.user_id == user_id)
    if session_id:
        stmt = stmt.where(Conversation.session_id == session_id)
    stmt = stmt.order_by(Conversation.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(stmt)
    rows = list(reversed(result.scalars().all()))
    return [
        {"role": r.role, "content": r.content, "created_at": r.created_at.isoformat(), "session_id": r.session_id}
        for r in rows
    ]


@router.delete("/conversations/{user_id}/cleanup")
async def cleanup_old_conversations(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    cutoff = datetime.now(timezone.utc) - timedelta(days=SESSION_EXPIRE_DAYS)
    result = await db.execute(
        delete(Conversation)
        .where(Conversation.user_id == user_id, Conversation.created_at < cutoff)
    )
    await db.commit()
    return {"deleted": result.rowcount}
