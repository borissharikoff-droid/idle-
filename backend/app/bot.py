"""
Telegram bot using aiogram.

Provides /start command and Mini App launch button.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    WebAppInfo
)

from app.config import settings
from app.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def get_webapp_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard with Mini App button."""
    webapp_url = settings.WEBAPP_URL
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⛏️ Play Idle Mining",
                web_app=WebAppInfo(url=webapp_url)
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Leaderboard",
                callback_data="leaderboard"
            ),
            InlineKeyboardButton(
                text="❓ Help",
                callback_data="help"
            )
        ]
    ])
    
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command."""
    user = message.from_user
    
    welcome_text = f"""
⛏️ **Welcome to Idle Mining Game!**

Hey {user.first_name}! Ready to become a master miner?

🎮 **How to Play:**
• Click the button below to open the game
• Select an ore to mine
• Watch your XP and level grow!

📈 **Features:**
• 5 different ores to discover
• 100 levels to achieve
• Compete with other players

_Inspired by OSRS & Melvor Idle_

Tap the button below to start your mining adventure!
"""
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_webapp_keyboard()
    )


@dp.callback_query(lambda c: c.data == "help")
async def callback_help(callback: types.CallbackQuery):
    """Handle help button."""
    help_text = """
📖 **Idle Mining Guide**

**Mining Basics:**
• Select an ore to start mining
• Mining continues automatically
• Each ore gives XP when mined
• Level up to unlock new ores

**Ores:**
🟤 Copper (Lv.1) - 10 XP
⚪ Iron (Lv.15) - 25 XP
🔘 Silver (Lv.30) - 45 XP
🟡 Gold (Lv.50) - 75 XP
🔵 Mithril (Lv.70) - 120 XP

**Tips:**
• Higher level ores give more XP
• Keep mining to level up faster
• Check the leaderboard to compete!
"""
    
    await callback.message.answer(help_text, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(lambda c: c.data == "leaderboard")
async def callback_leaderboard(callback: types.CallbackQuery):
    """Handle leaderboard button."""
    # TODO: Implement actual leaderboard from database
    leaderboard_text = """
🏆 **Mining Leaderboard**

_Coming soon!_

Top miners will be displayed here.
Keep mining to climb the ranks!
"""
    
    await callback.message.answer(leaderboard_text, parse_mode="Markdown")
    await callback.answer()


async def main():
    """Start the bot."""
    logger.info("Starting bot...")
    await init_db()
    logger.info("Database initialized!")
    
    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
