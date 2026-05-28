from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.models.schemas import IntimacyResponse
from server.services.intimacy_service import compute_score, get_level, get_next_milestone

router = APIRouter(prefix="/api/intimacy", tags=["intimacy"])


@router.get("/{user_id}", response_model=IntimacyResponse)
async def get_intimacy(user_id: str, db: AsyncSession = Depends(get_db)):
    score = await compute_score(db, user_id)
    return IntimacyResponse(
        user_id=user_id,
        score=score,
        level=get_level(score),
        next_milestone=get_next_milestone(score),
    )
