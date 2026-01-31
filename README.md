# Idle Mining Game - Telegram Mini App

A multiplayer idle mining game inspired by OSRS and Melvor Idle, built as a Telegram Mini App.

## Features

- ⛏️ Mining skill with 5 ores (Copper, Iron, Silver, Gold, Mithril)
- 📈 100 levels with OSRS-style XP progression
- 🎮 Real-time mining with progress bar
- 🌐 WebSocket-based live updates
- 📱 Telegram Mini App integration

## Tech Stack

- **Backend**: Python, FastAPI, aiogram, SQLAlchemy
- **Frontend**: React, TypeScript, Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Railway

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (or Docker)

### Quick Start with Docker

```bash
# Set your bot token
export BOT_TOKEN=your_bot_token_here

# Start all services
docker-compose up -d
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/idlzga
export BOT_TOKEN=your_bot_token_here
export WEBAPP_URL=http://localhost:3000

# Run the server
python -m app.main
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
echo "VITE_WS_URL=ws://localhost:8000" >> .env

# Run development server
npm run dev
```

## Deployment to Railway

### 1. Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Add PostgreSQL database

### 2. Deploy Backend

1. Connect your GitHub repo
2. Select the `backend` folder
3. Add environment variables:
   - `BOT_TOKEN`: Your Telegram bot token
   - `WEBAPP_URL`: Your frontend URL (set after frontend deploy)
   - `DATABASE_URL`: Will be auto-filled by Railway

### 3. Deploy Frontend

1. Add new service from same repo
2. Select the `frontend` folder
3. Add environment variables:
   - `VITE_API_URL`: Your backend URL
   - `VITE_WS_URL`: Your backend URL (wss://)

### 4. Configure Telegram Bot

1. Open [@BotFather](https://t.me/BotFather)
2. Send `/mybots` and select your bot
3. Go to "Bot Settings" → "Menu Button"
4. Set your Mini App URL (frontend URL)

Or configure via `/setmenubutton`:
```
/setmenubutton
```
Then enter your frontend URL.

## Project Structure

```
idlzga/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── bot.py           # Telegram bot
│   │   ├── config.py        # Settings
│   │   ├── database.py      # DB setup
│   │   ├── models/          # SQLAlchemy models
│   │   ├── game/            # Game logic
│   │   │   ├── data/        # Ores, XP table
│   │   │   └── skills/      # Mining skill
│   │   └── routers/         # API endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main app
│   │   ├── components/      # UI components
│   │   └── hooks/           # React hooks
│   └── package.json
└── docker-compose.yml
```

## Game Mechanics

### XP/Level System

Uses OSRS-style exponential XP curve:
- Level 1: 0 XP
- Level 50: ~101,333 XP
- Level 100: ~13,034,431 XP

### Ores

| Ore     | Level | XP  | Time  |
|---------|-------|-----|-------|
| Copper  | 1     | 10  | 2.0s  |
| Iron    | 15    | 25  | 3.5s  |
| Silver  | 30    | 45  | 5.0s  |
| Gold    | 50    | 75  | 7.0s  |
| Mithril | 70    | 120 | 10.0s |

## Future Features

- 🤝 Trading between players
- 💬 In-game chat
- 👥 Party system
- 🐉 Boss fights
- 🔨 More skills (Smithing, Woodcutting, etc.)
- 🏆 Leaderboards

## License

MIT
