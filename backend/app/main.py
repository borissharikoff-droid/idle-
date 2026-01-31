"""
Main FastAPI application.

Combines REST API, WebSocket, and initializes the database.
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import auth_router, game_router
from app.routers.websocket import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("Starting up...")
    await init_db()
    print("Database initialized!")
    
    yield
    
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Idle Mining Game",
    description="A multiplayer idle mining game inspired by OSRS and Melvor Idle",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(game_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "game": "Idle Mining Game",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check for Railway."""
    return {"status": "healthy"}


@app.websocket("/ws/{user_id}")
async def websocket_route(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time game updates."""
    await websocket_endpoint(websocket, user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
