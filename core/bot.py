from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from core.handlers import BotHandlers
from config.settings import settings
from utils.logger import logger

class TelegramBot:
    """Main Telegram Bot class"""
    
    def __init__(self):
        self.handlers = BotHandlers()
        self.app = None
        
    def setup_handlers(self):
        """Setup all handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.handlers.start_command))
        
        # Callback handlers
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.language_callback,
            pattern="^lang_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.start_bot_callback,
            pattern="^start_bot$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.test_bot_callback,
            pattern="^test_bot$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.verify_id_callback,
            pattern="^verify_id$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.get_signal_callback,
            pattern="^get_signal$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.back_to_menu_callback,
            pattern="^back_to_menu$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.stop_signals_callback,
            pattern="^stop_signals$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.handlers.connect_account_callback,
            pattern="^connect_account$"
        ))
        
        # Message handler for text input
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handlers.handle_text_input
        ))
    
    async def run(self):
        """Run the bot"""
        try:
            # Create application
            self.app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
            
            # Setup handlers
            self.setup_handlers()
            
            # Log startup
            logger.info("Bot started successfully!")
            logger.info(f"Admin IDs: {settings.ADMIN_IDS}")
            
            # Start polling
            await self.app.run_polling()
            
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise
