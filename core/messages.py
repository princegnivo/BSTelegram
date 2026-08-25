WELCOME_MESSAGE = """👋 Bonjour
Choisissez votre langue préférée.
Vous pouvez modifier la langue à tout moment depuis le menu principal"""

MAIN_MESSAGE = """LEGITTRADE Bot qui traite les données de marché en temps réel sur toutes les principales paires de devises et identifie des points d'entrée structurés à la demande.

Développé par une équipe dédiée de développeurs et d'analystes de marché.

L'accès est basé sur des niveaux et lié au volume de trading actif sur Pocket Option."""

USER_MENU_MESSAGE = """LEGITTRADE Bot analyse les tendances du marché à court terme et fournit des setups de trading structurés en temps réel - directement sur Telegram.

📊 Point d'entrée
📈 Actif
🎯 Direction
⏱ Durée

✨ Une session d'essai limitée est disponible pour les nouveaux utilisateurs."""

TEST_BOT_MESSAGE = """Pour tester le bot, veuillez connecter un compte.

⚠️ Les comptes existants ne sont pas pris en charge."""

VERIFY_ID_MESSAGE = """🔑 Entrez votre ID Pocket Option.

📌 Chiffres uniquement."""

def format_signal_message(signal_data: dict) -> str:
    """Format signal message for Telegram"""
    direction_emoji = "🟢" if signal_data['direction'] == 'CALL' else "🔴"
    direction_text = "ACHAT (CALL)" if signal_data['direction'] == 'CALL' else "VENTE (PUT)"
    
    message = f"""
{direction_emoji} **SIGNAL {direction_text}** {direction_emoji}
-----------------------------------

📊 **ACTIF**: {signal_data['asset']}
🕘 **HEURE D'ENTRÉE**: {signal_data['entry_time']}
⏳ **EXPIRATION**: {signal_data['expiration']}

🔮 **Direction**: {direction_text}

💡 **Indicateurs**:
• Bollinger Bands: {signal_data.get('bb_signal', 'N/A')}
• MACD: {signal_data.get('macd_signal', 'N/A')}
• RSI: {signal_data.get('rsi', 'N/A')}

📈 **Prix d'entrée**: {signal_data.get('entry_price', 'N/A')}
"""
    return message
