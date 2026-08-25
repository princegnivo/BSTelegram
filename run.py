#!/usr/bin/env python3
"""
Entry point for the Pocket Signal Bot
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check token
if not os.getenv("TELEGRAM_BOT_TOKEN"):
    print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env file")
    print("Please create a .env file with your bot token")
    sys.exit(1)

# Run bot
from main import main

if __name__ == "__main__":
    main()
