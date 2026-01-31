"""
Development runner - starts both FastAPI and Bot.
"""

import asyncio
import uvicorn
from multiprocessing import Process


def run_api():
    """Run FastAPI server."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


def run_bot():
    """Run Telegram bot."""
    import asyncio
    from app.bot import main
    asyncio.run(main())


if __name__ == "__main__":
    # Start API in a separate process
    api_process = Process(target=run_api)
    api_process.start()
    
    # Run bot in main process
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        api_process.terminate()
        api_process.join()
