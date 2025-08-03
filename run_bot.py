#!/usr/bin/env python3
"""
Simple wrapper to run PMO Recovery Bot
"""

import sys
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Run the bot"""
    try:
        logger.info("🚀 Starting PMO Recovery Bot...")
        
        # Import main components
        from telegram.ext import Application
        from config.settings import Settings
        
        logger.info(f"✅ Bot Token: {Settings.BOT_TOKEN[:10]}...")
        
        # Create application
        application = Application.builder().token(Settings.BOT_TOKEN).build()
        
        # Add basic start handler for testing
        from telegram import Update
        from telegram.ext import ContextTypes, CommandHandler
        
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command"""
            await update.message.reply_text(
                "🤖 PMO Recovery Bot is running!\n"
                "All components loaded successfully."
            )
        
        application.add_handler(CommandHandler("start", start_command))
        
        logger.info("✅ Bot configured successfully!")
        logger.info("🏃 Starting polling...")
        
        # Run the bot
        application.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
