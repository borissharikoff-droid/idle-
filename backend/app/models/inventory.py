from sqlalchemy import BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class InventoryItem(Base):
    __tablename__ = "inventory"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        index=True
    )
    item_type: Mapped[str] = mapped_column(String(50), index=True)  # e.g., "copper_ore"
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="inventory")
    
    def __repr__(self) -> str:
        return f"<InventoryItem {self.item_type} x{self.quantity}>"
