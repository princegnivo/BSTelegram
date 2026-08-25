import asyncio
import sys
from core.bot import TelegramBot
from utils.logger import logger

async def main():
    """Main entry point"""
    try:
        bot = TelegramBot()
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
