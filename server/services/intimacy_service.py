from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.db_models import IntimacyEvent

SCORE_MAP = {
    "chat": 2,
    "memory_share": 5,
    "return_visit": 10,
    "task_complete": 3,
}

LEVELS = [
    (30, "初识"),
    (60, "熟悉"),
    (90, "亲近"),
    (999, "默契"),
]


async def compute_score(db: AsyncSession, user_id: str) -> int:
    result = await db.execute(
        select(func.coalesce(func.sum(IntimacyEvent.score_delta), 0))
        .where(IntimacyEvent.user_id == user_id)
    )
    return int(result.scalar())


async def record_event(
    db: AsyncSession,
    user_id: str,
    event_type: str,
) -> int:
    delta = SCORE_MAP.get(event_type, 1)

    now = datetime.now(timezone.utc)
    three_days_ago = now - timedelta(days=3)
    streak_result = await db.execute(
        select(func.count(func.distinct(func.date(IntimacyEvent.created_at))))
        .where(
            IntimacyEvent.user_id == user_id,
            IntimacyEvent.created_at >= three_days_ago,
        )
    )
    streak_days = streak_result.scalar() or 0
    if streak_days >= 3:
        delta = int(delta * 1.5)

    event = IntimacyEvent(
        user_id=user_id,
        event_type=event_type,
        score_delta=delta,
    )
    db.add(event)
    await db.flush()
    return delta


def get_level(score: int) -> str:
    for threshold, name in LEVELS:
        if score < threshold:
            return name
    return "默契"


def get_next_milestone(score: int) -> int:
    for threshold, _ in LEVELS:
        if score < threshold:
            return threshold
    return score
