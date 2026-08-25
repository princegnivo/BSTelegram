from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_language_keyboard():
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    """Main menu keyboard after language selection"""
    keyboard = [
        [InlineKeyboardButton("🚀 Commencer", callback_data="start_bot")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_user_menu_keyboard():
    """User menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🧪 Tester le bot", callback_data="test_bot"),
            InlineKeyboardButton("🔗 Connecter un compte", callback_data="connect_account")
        ],
        [
            InlineKeyboardButton("💎 Avoir signal", callback_data="get_signal")
        ],
        [
            InlineKeyboardButton("🆘 Soutien", url="https://t.me/PrinceRoyal_1"),
            InlineKeyboardButton("📢 Canal", url="https://t.me/your_channel")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_account_management_keyboard():
    """Account management keyboard"""
    keyboard = [
        [InlineKeyboardButton("➕ Créer un compte", url="https://pocketoption.com")],
        [InlineKeyboardButton("✅ Vérifier le nouvel ID", callback_data="verify_id")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Back button keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Retour", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_signal_control_keyboard():
    """Signal control keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔄 Actualiser", callback_data="refresh_signals")],
        [InlineKeyboardButton("⏹ Arrêter les signaux", callback_data="stop_signals")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
