"""
Authentication router for Telegram Mini App.

Validates Telegram WebApp initData and creates/retrieves users.
"""

import hashlib
import hmac
import json
from urllib.parse import parse_qs, unquote
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


class TelegramAuthData(BaseModel):
    init_data: str


class UserResponse(BaseModel):
    telegram_id: int
    username: str | None
    first_name: str | None
    
    class Config:
        from_attributes = True


def validate_telegram_data(init_data: str) -> dict | None:
    """
    Validate Telegram WebApp initData.
    Returns parsed user data if valid, None otherwise.
    """
    try:
        parsed = parse_qs(init_data)
        
        # Extract hash
        received_hash = parsed.get("hash", [None])[0]
        if not received_hash:
            return None
        
        # Build data check string
        data_pairs = []
        for key, value in parsed.items():
            if key != "hash":
                data_pairs.append(f"{key}={value[0]}")
        data_pairs.sort()
        data_check_string = "\n".join(data_pairs)
        
        # Calculate secret key
        secret_key = hmac.new(
            b"WebAppData",
            settings.BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Validate
        if calculated_hash != received_hash:
            return None
        
        # Parse user data
        user_data = parsed.get("user", [None])[0]
        if user_data:
            return json.loads(unquote(user_data))
        
        return None
    except Exception:
        return None


@router.post("/telegram", response_model=UserResponse)
async def authenticate_telegram(
    auth_data: TelegramAuthData,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user via Telegram WebApp initData.
    Creates user if not exists.
    """
    # For development, allow bypassing validation
    user_data = validate_telegram_data(auth_data.init_data)
    
    # If validation fails, try parsing as JSON (for dev)
    if not user_data:
        try:
            user_data = json.loads(auth_data.init_data)
        except:
            raise HTTPException(status_code=401, detail="Invalid authentication data")
    
    telegram_id = user_data.get("id")
    if not telegram_id:
        raise HTTPException(status_code=401, detail="Invalid user data")
    
    # Get or create user
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=user_data.get("username"),
            first_name=user_data.get("first_name")
        )
        db.add(user)
        await db.flush()
    else:
        # Update user info
        user.username = user_data.get("username")
        user.first_name = user_data.get("first_name")
        await db.flush()
    
    return user
