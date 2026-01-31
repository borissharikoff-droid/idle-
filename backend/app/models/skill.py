from sqlalchemy import BigInteger, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        index=True
    )
    skill_type: Mapped[str] = mapped_column(String(50), index=True)  # e.g., "mining"
    xp: Mapped[int] = mapped_column(BigInteger, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    
    # Current action tracking
    current_action: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g., "copper"
    action_started: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="skills")
    
    def __repr__(self) -> str:
        return f"<Skill {self.skill_type} Lv.{self.level} ({self.xp} XP)>"
