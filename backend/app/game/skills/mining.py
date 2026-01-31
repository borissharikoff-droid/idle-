"""
Mining skill logic.

Handles mining operations, XP gains, and level ups.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Skill, InventoryItem
from app.game.data.ores import get_ore, get_available_ores, Ore
from app.game.data.xp_table import get_level_for_xp, get_xp_to_next_level


@dataclass
class MiningResult:
    success: bool
    ore_mined: bool = False
    ore_id: str | None = None
    ore_name: str | None = None
    xp_gained: int = 0
    total_xp: int = 0
    level: int = 1
    leveled_up: bool = False
    new_level: int | None = None
    ore_quantity: int = 0
    progress: float = 0.0  # 0.0 to 1.0
    xp_in_level: int = 0
    xp_needed: int = 0
    message: str = ""


class MiningSkill:
    SKILL_TYPE = "mining"
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_or_create_skill(self, user_id: int) -> Skill:
        """Get or create mining skill for user."""
        result = await self.db.execute(
            select(Skill).where(
                Skill.user_id == user_id,
                Skill.skill_type == self.SKILL_TYPE
            )
        )
        skill = result.scalar_one_or_none()
        
        if not skill:
            skill = Skill(
                user_id=user_id,
                skill_type=self.SKILL_TYPE,
                xp=0,
                level=1
            )
            self.db.add(skill)
            await self.db.flush()
        
        return skill
    
    async def get_inventory_item(self, user_id: int, item_type: str) -> InventoryItem:
        """Get or create inventory item."""
        result = await self.db.execute(
            select(InventoryItem).where(
                InventoryItem.user_id == user_id,
                InventoryItem.item_type == item_type
            )
        )
        item = result.scalar_one_or_none()
        
        if not item:
            item = InventoryItem(
                user_id=user_id,
                item_type=item_type,
                quantity=0
            )
            self.db.add(item)
            await self.db.flush()
        
        return item
    
    async def start_mining(self, user_id: int, ore_id: str) -> MiningResult:
        """Start mining a specific ore."""
        skill = await self.get_or_create_skill(user_id)
        ore = get_ore(ore_id)
        
        if not ore:
            return MiningResult(
                success=False,
                message=f"Unknown ore: {ore_id}"
            )
        
        if skill.level < ore.level_required:
            return MiningResult(
                success=False,
                message=f"You need Mining level {ore.level_required} to mine {ore.name}."
            )
        
        # Set current action
        skill.current_action = ore_id
        skill.action_started = datetime.now(timezone.utc)
        await self.db.flush()
        
        xp_in_level, xp_needed = get_xp_to_next_level(skill.xp, skill.level)
        
        return MiningResult(
            success=True,
            ore_id=ore_id,
            ore_name=ore.name,
            total_xp=skill.xp,
            level=skill.level,
            progress=0.0,
            xp_in_level=xp_in_level,
            xp_needed=xp_needed,
            message=f"Started mining {ore.name}..."
        )
    
    async def stop_mining(self, user_id: int) -> MiningResult:
        """Stop mining."""
        skill = await self.get_or_create_skill(user_id)
        
        skill.current_action = None
        skill.action_started = None
        await self.db.flush()
        
        xp_in_level, xp_needed = get_xp_to_next_level(skill.xp, skill.level)
        
        return MiningResult(
            success=True,
            total_xp=skill.xp,
            level=skill.level,
            xp_in_level=xp_in_level,
            xp_needed=xp_needed,
            message="Mining stopped."
        )
    
    async def process_mining_tick(self, user_id: int) -> MiningResult | None:
        """
        Process a mining tick. Called periodically while user is mining.
        Returns MiningResult if ore was mined, None if still in progress.
        """
        skill = await self.get_or_create_skill(user_id)
        
        if not skill.current_action or not skill.action_started:
            return None
        
        ore = get_ore(skill.current_action)
        if not ore:
            return None
        
        now = datetime.now(timezone.utc)
        elapsed = (now - skill.action_started).total_seconds()
        progress = min(elapsed / ore.mining_time, 1.0)
        
        xp_in_level, xp_needed = get_xp_to_next_level(skill.xp, skill.level)
        
        # Check if mining is complete
        if elapsed >= ore.mining_time:
            # Award ore
            item = await self.get_inventory_item(user_id, f"{ore.id}_ore")
            item.quantity += 1
            
            # Award XP
            old_level = skill.level
            skill.xp += ore.xp
            new_level = get_level_for_xp(skill.xp)
            leveled_up = new_level > old_level
            
            if leveled_up:
                skill.level = new_level
            
            # Reset action timer for next ore
            skill.action_started = datetime.now(timezone.utc)
            await self.db.flush()
            
            xp_in_level, xp_needed = get_xp_to_next_level(skill.xp, skill.level)
            
            return MiningResult(
                success=True,
                ore_mined=True,
                ore_id=ore.id,
                ore_name=ore.name,
                xp_gained=ore.xp,
                total_xp=skill.xp,
                level=skill.level,
                leveled_up=leveled_up,
                new_level=new_level if leveled_up else None,
                ore_quantity=item.quantity,
                progress=0.0,  # Reset progress
                xp_in_level=xp_in_level,
                xp_needed=xp_needed,
                message=f"+1 {ore.name}! +{ore.xp} XP"
            )
        
        # Still mining - return progress
        return MiningResult(
            success=True,
            ore_mined=False,
            ore_id=ore.id,
            ore_name=ore.name,
            total_xp=skill.xp,
            level=skill.level,
            progress=progress,
            xp_in_level=xp_in_level,
            xp_needed=xp_needed,
            message=f"Mining {ore.name}..."
        )
    
    async def get_status(self, user_id: int) -> dict:
        """Get current mining status."""
        skill = await self.get_or_create_skill(user_id)
        
        xp_in_level, xp_needed = get_xp_to_next_level(skill.xp, skill.level)
        available_ores = get_available_ores(skill.level)
        
        # Get inventory counts for ores
        inventory = {}
        for ore in available_ores:
            item = await self.get_inventory_item(user_id, f"{ore.id}_ore")
            inventory[ore.id] = item.quantity
        
        return {
            "skill_type": self.SKILL_TYPE,
            "level": skill.level,
            "xp": skill.xp,
            "xp_in_level": xp_in_level,
            "xp_needed": xp_needed,
            "current_action": skill.current_action,
            "action_started": skill.action_started.isoformat() if skill.action_started else None,
            "available_ores": [
                {
                    "id": ore.id,
                    "name": ore.name,
                    "level_required": ore.level_required,
                    "xp": ore.xp,
                    "mining_time": ore.mining_time,
                    "ascii": ore.ascii,
                    "color": ore.color,
                    "description": ore.description,
                    "quantity": inventory.get(ore.id, 0),
                    "unlocked": skill.level >= ore.level_required
                }
                for ore in get_available_ores(100)  # Show all ores
            ],
            "inventory": inventory
        }
