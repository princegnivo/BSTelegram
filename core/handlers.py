import asyncio
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from core.keyboards import *
from core.messages import *
from trading.strategy import TradingStrategy
from api.pocket_client import PocketOptionClient
from utils.logger import logger
from config.settings import settings
import pandas as pd

# Global state
user_data = {}
signal_tasks = {}

class BotHandlers:
    """Handlers for bot commands and callbacks"""
    
    def __init__(self):
        self.strategy = TradingStrategy()
        self.pocket = PocketOptionClient()
        self.signal_generation = {}
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        # Initialize user data
        user_data[user_id] = {
            'language': None,
            'account_verified': False,
            'pocket_id': None,
            'signals_active': False,
            'last_signal': None
        }
        
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=get_language_keyboard()
        )
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        language = query.data.split('_')[1]
        
        user_data[user_id]['language'] = language
        
        # Send main message with image
        await query.edit_message_text(
            MAIN_MESSAGE,
            reply_markup=get_main_menu_keyboard()
        )
        
        # Send image (replace with your image path)
        # await context.bot.send_photo(
        #     chat_id=update.effective_chat.id,
        #     photo=open('data/images/main.png', 'rb'),
        #     caption=MAIN_MESSAGE,
        #     reply_markup=get_main_menu_keyboard()
        # )
    
    async def start_bot_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle start bot button"""
        query = update.callback_query
        await query.answer()
        
        # Send user menu
        await query.edit_message_text(
            USER_MENU_MESSAGE,
            reply_markup=get_user_menu_keyboard()
        )
    
    async def test_bot_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle test bot button"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            TEST_BOT_MESSAGE,
            reply_markup=get_account_management_keyboard()
        )
    
    async def verify_id_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle verify ID button"""
        query = update.callback_query
        await query.answer()
        
        # Send image for verification
        # await context.bot.send_photo(
        #     chat_id=update.effective_chat.id,
        #     photo=open('data/images/verify.png', 'rb'),
        #     caption=VERIFY_ID_MESSAGE,
        #     reply_markup=get_back_keyboard()
        # )
        
        await query.edit_message_text(
            VERIFY_ID_MESSAGE,
            reply_markup=get_back_keyboard()
        )
        
        # Set state to wait for ID input
        user_id = update.effective_user.id
        user_data[user_id]['awaiting_id'] = True
    
    async def handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (ID input)"""
        user_id = update.effective_user.id
        
        if user_data.get(user_id, {}).get('awaiting_id'):
            pocket_id = update.message.text.strip()
            
            if pocket_id.isdigit():
                user_data[user_id]['pocket_id'] = pocket_id
                user_data[user_id]['account_verified'] = True
                user_data[user_id]['awaiting_id'] = False
                
                await update.message.reply_text(
                    f"✅ ID {pocket_id} vérifié avec succès!\n"
                    "Vous pouvez maintenant recevoir des signaux.",
                    reply_markup=get_user_menu_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Veuillez entrer uniquement des chiffres.",
                    reply_markup=get_back_keyboard()
                )
    
    async def get_signal_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle get signal button"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        
        if not user_data.get(user_id, {}).get('account_verified'):
            await query.edit_message_text(
                "⚠️ Veuillez d'abord vérifier votre ID Pocket Option.",
                reply_markup=get_account_management_keyboard()
            )
            return
        
        # Start signal generation
        if user_id not in signal_tasks or signal_tasks[user_id].done():
            signal_tasks[user_id] = asyncio.create_task(
                self.generate_signals(update, context)
            )
            user_data[user_id]['signals_active'] = True
            
            await query.edit_message_text(
                "🔍 Analyse en cours...⏳\n\n"
                "Recherche de signaux sur les paires OTC avec payout ≥ 87%\n"
                "📊 Timeframes: 1m, 2m, 5m",
                reply_markup=get_signal_control_keyboard()
            )
        else:
            await query.answer("Les signaux sont déjà en cours d'analyse...")
    
    async def generate_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate trading signals in real-time"""
        user_id = update.effective_user.id
        
        try:
            # Connect to Pocket Option
            await self.pocket.connect()
            
            # Get available assets
            assets = await self.pocket.get_assets()
            
            # Filter OTC assets with payout >= 87%
            eligible_assets = []
            for asset, info in assets.items():
                if info.get('is_otc', False):
                    payout = await self.pocket.get_payout(asset, "1m")
                    if payout and payout >= settings.MIN_PAYOUT:
                        eligible_assets.append(asset)
            
            logger.info(f"Eligible assets: {eligible_assets}")
            
            while user_data.get(user_id, {}).get('signals_active', False):
                for asset in eligible_assets[:5]:  # Limit to 5 assets for performance
                    # Get candles for each timeframe
                    for timeframe, duration in settings.TIMEFRAMES.items():
                        df = await self.pocket.get_candles(asset, duration, 100)
                        
                        if df.empty:
                            continue
                        
                        # Analyze based on timeframe
                        signal = None
                        if timeframe == "1m":
                            signal = self.strategy.analyze_1m(df)
                        elif timeframe == "2m":
                            signal = self.strategy.analyze_2m(df)
                        elif timeframe == "5m":
                            signal = self.strategy.analyze_5m(df)
                        
                        # Send signal if conditions met
                        if signal and (signal.get('call') or signal.get('put')):
                            direction = "CALL" if signal.get('call') else "PUT"
                            
                            signal_data = {
                                'asset': asset,
                                'direction': direction,
                                'entry_time': datetime.now().strftime('%H:%M'),
                                'expiration': f"{duration}M",
                                'entry_price': df['close'].iloc[-1],
                                'bb_signal': f"Band {'Lower' if direction == 'CALL' else 'Upper'}",
                                'macd_signal': signal.get('macd', 'N/A'),
                                'rsi': round(signal.get('rsi', 0), 2)
                            }
                            
                            # Format and send signal
                            signal_message = format_signal_message(signal_data)
                            
                            await context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=signal_message,
                                parse_mode='Markdown'
                            )
                            
                            user_data[user_id]['last_signal'] = signal_data
                            
                            # Wait 30 seconds between signals
                            await asyncio.sleep(30)
                
                # Wait before next iteration
                await asyncio.sleep(10)
                
        except Exception as e:
            logger.error(f"Error in signal generation: {e}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Erreur dans la génération des signaux: {str(e)}"
            )
    
    async def back_to_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle back to menu button"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            USER_MENU_MESSAGE,
            reply_markup=get_user_menu_keyboard()
        )
    
    async def stop_signals_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle stop signals button"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        
        if user_id in signal_tasks:
            signal_tasks[user_id].cancel()
            user_data[user_id]['signals_active'] = False
            
            await query.edit_message_text(
                "⏹ Signaux arrêtés.",
                reply_markup=get_user_menu_keyboard()
            )
