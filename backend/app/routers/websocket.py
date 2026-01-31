"""
WebSocket handler for real-time game updates.

Manages mining progress ticks and broadcasts updates to connected clients.
"""

import asyncio
import json
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.game.skills.mining import MiningSkill


class ConnectionManager:
    """Manages WebSocket connections and game loops."""
    
    def __init__(self):
        # user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
        # user_id -> asyncio.Task (mining loop)
        self.mining_tasks: Dict[int, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new connection."""
        await websocket.accept()
        
        # Disconnect existing connection if any
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
            except:
                pass
        
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        """Remove a connection."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Cancel mining task if running
        if user_id in self.mining_tasks:
            self.mining_tasks[user_id].cancel()
            del self.mining_tasks[user_id]
    
    async def send_message(self, user_id: int, message: dict):
        """Send a message to a specific user."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                self.disconnect(user_id)
    
    async def start_mining_loop(self, user_id: int, ore_id: str):
        """Start the mining loop for a user."""
        # Cancel existing task if any
        if user_id in self.mining_tasks:
            self.mining_tasks[user_id].cancel()
        
        # Create new mining task
        task = asyncio.create_task(self._mining_loop(user_id, ore_id))
        self.mining_tasks[user_id] = task
    
    def stop_mining_loop(self, user_id: int):
        """Stop the mining loop for a user."""
        if user_id in self.mining_tasks:
            self.mining_tasks[user_id].cancel()
            del self.mining_tasks[user_id]
    
    async def _mining_loop(self, user_id: int, ore_id: str):
        """Internal mining loop that sends progress updates."""
        try:
            while True:
                async with async_session() as db:
                    mining = MiningSkill(db)
                    result = await mining.process_mining_tick(user_id)
                    await db.commit()
                    
                    if result is None:
                        # No longer mining
                        break
                    
                    if result.ore_mined:
                        # Ore was mined
                        message = {
                            "type": "ore_mined",
                            "ore_id": result.ore_id,
                            "ore_name": result.ore_name,
                            "xp_gained": result.xp_gained,
                            "total_xp": result.total_xp,
                            "level": result.level,
                            "ore_quantity": result.ore_quantity,
                            "xp_in_level": result.xp_in_level,
                            "xp_needed": result.xp_needed,
                            "message": result.message
                        }
                        await self.send_message(user_id, message)
                        
                        if result.leveled_up:
                            await self.send_message(user_id, {
                                "type": "level_up",
                                "skill": "mining",
                                "new_level": result.new_level
                            })
                    else:
                        # Progress update
                        await self.send_message(user_id, {
                            "type": "mining_tick",
                            "progress": result.progress,
                            "ore_id": result.ore_id,
                            "ore_name": result.ore_name
                        })
                
                # Tick rate: 100ms for smooth progress bar
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self.send_message(user_id, {
                "type": "error",
                "message": str(e)
            })


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Main WebSocket endpoint handler."""
    await manager.connect(websocket, user_id)
    
    try:
        # Send initial status
        async with async_session() as db:
            mining = MiningSkill(db)
            status = await mining.get_status(user_id)
            await websocket.send_json({
                "type": "status",
                "data": status
            })
            
            # Resume mining if was mining
            if status["current_action"]:
                await manager.start_mining_loop(user_id, status["current_action"])
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            
            if action == "start_mining":
                ore_id = data.get("ore")
                if ore_id:
                    async with async_session() as db:
                        mining = MiningSkill(db)
                        result = await mining.start_mining(user_id, ore_id)
                        await db.commit()
                        
                        if result.success:
                            await manager.start_mining_loop(user_id, ore_id)
                            await websocket.send_json({
                                "type": "mining_started",
                                "ore_id": ore_id,
                                "ore_name": result.ore_name,
                                "message": result.message
                            })
                        else:
                            await websocket.send_json({
                                "type": "error",
                                "message": result.message
                            })
            
            elif action == "stop_mining":
                manager.stop_mining_loop(user_id)
                async with async_session() as db:
                    mining = MiningSkill(db)
                    result = await mining.stop_mining(user_id)
                    await db.commit()
                    
                    await websocket.send_json({
                        "type": "mining_stopped",
                        "message": result.message,
                        "level": result.level,
                        "xp": result.total_xp
                    })
            
            elif action == "get_status":
                async with async_session() as db:
                    mining = MiningSkill(db)
                    status = await mining.get_status(user_id)
                    await websocket.send_json({
                        "type": "status",
                        "data": status
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        manager.disconnect(user_id)
