import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.models.db_models import Conversation, Memory
from server.models.schemas import ChatRequest
from server.services.llm import stream_chat
from server.services.prompt_builder import build_system_prompt

router = APIRouter(prefix="/api", tags=["chat"])

HISTORY_LIMIT = 20


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
        await record_event(db, req.user_id, "chat")
        await db.commit()

    return StreamingResponse(generate(), media_type="text/event-stream")
