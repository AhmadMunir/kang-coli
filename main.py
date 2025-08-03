#!/usr/bin/env python3
"""
PMO Recovery Coach Telegram Bot
Main application entry point
"""

import asyncio
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config.settings import settings
from src.database.database import db
from src.bot.handlers.command_handlers import CommandHandlers
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.handlers.admin_handlers import AdminHandlers
from src.services.scheduler_service import SchedulerService
from src.utils.logger import app_logger

def setup_database_sync():
    """Initialize database and create tables (synchronous version)"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create database tables
        db.create_tables()
        app_logger.info("Database initialized successfully")
    except Exception as e:
        app_logger.error(f"Database initialization failed: {e}")
        raise

def setup_bot_handlers_sync(application: Application, scheduler_service: SchedulerService = None) -> None:
    """Setup bot command and callback handlers (synchronous version)"""
    
    # Initialize handlers
    command_handlers = CommandHandlers()
    callback_handlers = CallbackHandlers()
    admin_handlers = AdminHandlers(scheduler_service)
    
    # Add command handlers
    application.add_handler(CommandHandler("start", command_handlers.start_command))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    application.add_handler(CommandHandler("streak", command_handlers.streak_command))
    application.add_handler(CommandHandler("motivation", command_handlers.motivation_command))
    application.add_handler(CommandHandler("emergency", command_handlers.emergency_command))
    application.add_handler(CommandHandler("relapse", command_handlers.relapse_command))
    application.add_handler(CommandHandler("stats", command_handlers.stats_command))
    
    # Add admin command handlers
    application.add_handler(CommandHandler("broadcastnow", admin_handlers.broadcast_now_command))
    application.add_handler(CommandHandler("broadcaststats", admin_handlers.broadcast_stats_command))
    application.add_handler(CommandHandler("custombroadcast", admin_handlers.custom_broadcast_command))
    application.add_handler(CommandHandler("testbroadcast", admin_handlers.test_broadcast_command))
    application.add_handler(CommandHandler("weeklysummary", admin_handlers.weekly_summary_command))
    application.add_handler(CommandHandler("adminhelp", admin_handlers.admin_help_command))
    application.add_handler(CommandHandler("adminstats", admin_handlers.admin_stats_command))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
    
    app_logger.info("Bot handlers setup completed")

async def setup_database():
    """Initialize database and create tables"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create database tables
        db.create_tables()
        app_logger.info("Database initialized successfully")
    except Exception as e:
        app_logger.error(f"Database initialization failed: {e}")
        raise

async def setup_bot_handlers(application: Application) -> None:
    """Setup bot command and callback handlers"""
    
    # Initialize handlers
    command_handlers = CommandHandlers()
    callback_handlers = CallbackHandlers()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", command_handlers.start_command))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    application.add_handler(CommandHandler("streak", command_handlers.streak_command))
    application.add_handler(CommandHandler("motivation", command_handlers.motivation_command))
    application.add_handler(CommandHandler("emergency", command_handlers.emergency_command))
    application.add_handler(CommandHandler("relapse", command_handlers.relapse_command))
    application.add_handler(CommandHandler("stats", command_handlers.stats_command))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
    
    # Add message handler for text messages (for journaling, etc.)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text))
    
    app_logger.info("Bot handlers setup completed")

def main():
    """Main application function"""
    
    # Validate settings
    try:
        settings.validate()
        app_logger.info("Settings validation passed")
    except ValueError as e:
        app_logger.error(f"Settings validation failed: {e}")
        return
    
    # Setup database (synchronous)
    setup_database_sync()
    
    # Create bot application
    app_logger.info(f"Starting {settings.BOT_USERNAME}...")
    application = Application.builder().token(settings.BOT_TOKEN).build()
    
    # Setup and start scheduler for daily broadcasts
    scheduler_service = SchedulerService(application)
    scheduler_service.start_scheduler()
    app_logger.info("Daily broadcast scheduler started")
    
    # Setup handlers (synchronous) - pass scheduler to admin handlers
    setup_bot_handlers_sync(application, scheduler_service)
    
    # Start bot  
    app_logger.info("Bot is starting...")
    
    try:
        # Run the application
        application.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        app_logger.info("Shutting down bot...")
    finally:
        # Stop scheduler when bot stops
        scheduler_service.stop_scheduler()
        app_logger.info("Scheduler stopped")

if __name__ == "__main__":
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    try:
        # Run the bot (synchronous)
        main()
    except KeyboardInterrupt:
        app_logger.info("Bot stopped by user")
    except Exception as e:
        app_logger.error(f"Critical error: {e}")
        import sys
        sys.exit(1)
