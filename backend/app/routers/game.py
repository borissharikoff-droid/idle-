"""
Game API router.

Handles game state endpoints (REST fallback for non-WebSocket clients).
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.game.skills.mining import MiningSkill
from app.game.data.ores import get_all_ores

router = APIRouter(prefix="/game", tags=["game"])


class MiningActionRequest(BaseModel):
    user_id: int
    ore_id: str | None = None


class MiningStatusResponse(BaseModel):
    skill_type: str
    level: int
    xp: int
    xp_in_level: int
    xp_needed: int
    current_action: str | None
    action_started: str | None
    available_ores: list
    inventory: dict


@router.get("/mining/status")
async def get_mining_status(
    user_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get current mining skill status."""
    mining = MiningSkill(db)
    status = await mining.get_status(user_id)
    return status


@router.post("/mining/start")
async def start_mining(
    request: MiningActionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Start mining an ore."""
    mining = MiningSkill(db)
    result = await mining.start_mining(request.user_id, request.ore_id)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return {
        "success": True,
        "message": result.message,
        "ore_id": result.ore_id,
        "ore_name": result.ore_name,
        "level": result.level,
        "xp": result.total_xp
    }


@router.post("/mining/stop")
async def stop_mining(
    request: MiningActionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Stop mining."""
    mining = MiningSkill(db)
    result = await mining.stop_mining(request.user_id)
    
    return {
        "success": True,
        "message": result.message,
        "level": result.level,
        "xp": result.total_xp
    }


@router.get("/ores")
async def get_ores():
    """Get all ore definitions."""
    ores = get_all_ores()
    return [
        {
            "id": ore.id,
            "name": ore.name,
            "level_required": ore.level_required,
            "xp": ore.xp,
            "mining_time": ore.mining_time,
            "ascii": ore.ascii,
            "color": ore.color,
            "description": ore.description
        }
        for ore in ores
    ]
