import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Pocket Option
    POCKET_SSID: str = os.getenv("POCKET_SSID", "")
    POCKET_DEMO: bool = os.getenv("POCKET_DEMO", "true").lower() == "true"
    
    # Trading
    DEFAULT_AMOUNT: float = float(os.getenv("DEFAULT_AMOUNT", "1.0"))
    MIN_PAYOUT: int = int(os.getenv("MIN_PAYOUT", "87"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_RETENTION: str = os.getenv("LOG_RETENTION", "7 days")
    
    # Admin
    ADMIN_IDS: List[int] = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
    
    # Timeframes
    TIMEFRAMES = {
        "1m": 60,
        "2m": 120,
        "5m": 300
    }
    
    # Assets to monitor
    ASSETS = [
        "EURUSD_otc",
        "USDJPY_otc", 
        "GBPUSD_otc",
        "USDCHF_otc",
        "AUDUSD_otc",
        "USDCAD_otc",
        "EURJPY_otc",
        "GBPJPY_otc"
    ]

settings = Settings()
