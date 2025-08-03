"""
Backup and Restore Command Handlers for PMO Recovery Bot
Admin commands for data backup and recovery operations
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
import json
from datetime import datetime
from pathlib import Path

from ...services.backup_service import backup_service
from ...services.backup_scheduler import backup_scheduler
from ...utils.logger import app_logger

logger = app_logger

# Admin user IDs (you should set this in your config)
ADMIN_USER_IDS = {
    # Add your admin user IDs here, e.g.:
    # 123456789,  # Admin 1
    # 987654321,  # Admin 2
}

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_USER_IDS

async def backup_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show backup management menu (admin only)"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Access denied. Admin privileges required.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📦 Create Manual Backup", callback_data="backup_create_manual"),
            InlineKeyboardButton("🔄 Create Emergency Backup", callback_data="backup_create_emergency")
        ],
        [
            InlineKeyboardButton("📋 List Backups", callback_data="backup_list"),
            InlineKeyboardButton("📊 Backup Status", callback_data="backup_status")
        ],
        [
            InlineKeyboardButton("⚙️ Scheduler Settings", callback_data="backup_scheduler"),
            InlineKeyboardButton("🔧 Restore Menu", callback_data="backup_restore_menu")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="backup_close")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🗄️ **Backup Management Panel**\n\n"
        "Choose an option to manage your bot's data backups:\n\n"
        "📦 **Manual Backup** - Create backup now\n"
        "🔄 **Emergency Backup** - Quick backup for emergencies\n"
        "📋 **List Backups** - View all available backups\n"
        "📊 **Status** - Check backup system health\n"
        "⚙️ **Scheduler** - Manage automatic backups\n"
        "🔧 **Restore** - Restore from backup"
    )
    
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def backup_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle backup-related callback queries"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        await query.answer("❌ Access denied. Admin privileges required.")
        return
    
    await query.answer()
    data = query.data
    
    if data == "backup_create_manual":
        await handle_create_backup(query, "manual")
    elif data == "backup_create_emergency":
        await handle_create_backup(query, "emergency")
    elif data == "backup_list":
        await handle_list_backups(query)
    elif data == "backup_status":
        await handle_backup_status(query)
    elif data == "backup_scheduler":
        await handle_scheduler_settings(query)
    elif data == "backup_restore_menu":
        await handle_restore_menu(query)
    elif data == "backup_close":
        await query.edit_message_text("🗄️ Backup management panel closed.")
    elif data.startswith("backup_restore_"):
        await handle_restore_callback(query, data)
    elif data.startswith("backup_delete_"):
        await handle_delete_backup(query, data)

async def handle_create_backup(query, backup_type: str) -> None:
    """Handle backup creation"""
    await query.edit_message_text(f"⏳ Creating {backup_type} backup... Please wait.")
    
    try:
        success, result = await backup_service.create_full_backup(backup_type)
        
        if success:
            # Get backup file info
            backup_path = Path(result)
            file_size_mb = backup_path.stat().st_size / (1024 * 1024)
            
            message = (
                f"✅ **{backup_type.capitalize()} backup created successfully!**\n\n"
                f"📁 **File:** `{backup_path.name}`\n"
                f"📊 **Size:** {file_size_mb:.2f} MB\n"
                f"⏰ **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"💾 Backup saved to: `{result}`"
            )
            
            # Add back to menu button
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
        else:
            message = f"❌ **Backup failed:**\n\n`{result}`"
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        error_message = f"❌ **Backup error:**\n\n`{str(e)}`"
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(error_message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_list_backups(query) -> None:
    """Handle listing available backups"""
    await query.edit_message_text("📋 Loading backup list... Please wait.")
    
    try:
        backups = await backup_service.list_available_backups()
        
        message_parts = ["📋 **Available Backups:**\n"]
        buttons = []
        
        for backup_type, backup_list in backups.items():
            if backup_list:
                message_parts.append(f"\n**{backup_type.capitalize()} Backups:**")
                
                for i, backup in enumerate(backup_list[:3]):  # Show max 3 per type
                    age_days = int(backup['age_days'])
                    age_text = f"{age_days}d ago" if age_days > 0 else "Today"
                    
                    message_parts.append(
                        f"• `{backup['filename'][:30]}...` "
                        f"({backup['size_mb']:.1f}MB, {age_text})"
                    )
                    
                    # Add restore button for recent backups
                    if i < 2:  # Max 2 restore buttons per type
                        button_text = f"🔄 Restore {backup_type} #{i+1}"
                        callback_data = f"backup_restore_{backup_type}_{backup['filename']}"
                        buttons.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
                
                if len(backup_list) > 3:
                    message_parts.append(f"... and {len(backup_list) - 3} more")
        
        if not any(backups.values()):
            message_parts.append("\n📭 No backups found.")
        
        # Add navigation buttons
        buttons.extend([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")],
            [InlineKeyboardButton("❌ Close", callback_data="backup_close")]
        ])
        
        message = "\n".join(message_parts)
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        error_message = f"❌ **Error loading backups:**\n\n`{str(e)}`"
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(error_message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_backup_status(query) -> None:
    """Handle backup status display"""
    await query.edit_message_text("📊 Loading backup status... Please wait.")
    
    try:
        status = await backup_service.get_backup_status()
        scheduler_stats = backup_scheduler.get_backup_statistics()
        
        # Build status message
        message_parts = [
            "📊 **Backup System Status**\n",
            f"🗄️ **Database:** {'✅ Healthy' if status['database_integrity'] else '❌ Issues detected'}",
            f"💾 **DB Size:** {status['database_size_mb']:.2f} MB",
            f"📁 **Total Backups:** {status['total_backups']}",
            f"💽 **Backup Storage:** {status['backup_directory_size_mb']:.2f} MB",
        ]
        
        if status['latest_backup']:
            latest = status['latest_backup']
            message_parts.extend([
                f"\n🕒 **Latest Backup:**",
                f"• Type: {latest['type'].capitalize()}",
                f"• Created: {latest['created_at'][:19].replace('T', ' ')}",
                f"• Size: {latest['size_mb']:.2f} MB"
            ])
        
        # Scheduler status
        message_parts.extend([
            f"\n⚙️ **Scheduler:** {'🟢 Running' if scheduler_stats['scheduler_running'] else '🔴 Stopped'}",
            f"✅ **Successful:** {scheduler_stats['backup_stats']['successful_backups']}",
            f"❌ **Failed:** {scheduler_stats['backup_stats']['failed_backups']}"
        ])
        
        if scheduler_stats['next_daily_backup']:
            message_parts.append(f"⏰ **Next Daily:** {scheduler_stats['next_daily_backup']}")
        
        message = "\n".join(message_parts)
        
        # Add buttons
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="backup_status")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        error_message = f"❌ **Error loading status:**\n\n`{str(e)}`"
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(error_message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_scheduler_settings(query) -> None:
    """Handle scheduler settings"""
    scheduler_stats = backup_scheduler.get_backup_statistics()
    
    status_text = "🟢 Running" if scheduler_stats['scheduler_running'] else "🔴 Stopped"
    
    message = (
        f"⚙️ **Backup Scheduler Settings**\n\n"
        f"**Status:** {status_text}\n"
        f"**Successful Backups:** {scheduler_stats['backup_stats']['successful_backups']}\n"
        f"**Failed Backups:** {scheduler_stats['backup_stats']['failed_backups']}\n\n"
        f"**Schedule:**\n"
        f"• Daily: 03:00 AM\n"
        f"• Weekly: Sunday 02:00 AM\n\n"
        f"**Retention Policy:**\n"
        f"• Daily: 7 backups\n"
        f"• Weekly: 4 backups\n"
        f"• Manual: 10 backups\n"
        f"• Emergency: 3 backups"
    )
    
    buttons = []
    if scheduler_stats['scheduler_running']:
        buttons.append([InlineKeyboardButton("⏸️ Stop Scheduler", callback_data="backup_scheduler_stop")])
    else:
        buttons.append([InlineKeyboardButton("▶️ Start Scheduler", callback_data="backup_scheduler_start")])
    
    buttons.extend([
        [InlineKeyboardButton("🔄 Force Daily Backup", callback_data="backup_force_daily")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")]
    ])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_restore_menu(query) -> None:
    """Handle restore menu"""
    message = (
        "🔧 **Data Restore Menu**\n\n"
        "⚠️ **WARNING:** Restoring will replace current data!\n"
        "An emergency backup will be created before restore.\n\n"
        "Select backup type to restore from:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📅 Daily Backup", callback_data="backup_restore_list_daily"),
            InlineKeyboardButton("📆 Weekly Backup", callback_data="backup_restore_list_weekly")
        ],
        [
            InlineKeyboardButton("📝 Manual Backup", callback_data="backup_restore_list_manual"),
            InlineKeyboardButton("🚨 Emergency Backup", callback_data="backup_restore_list_emergency")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="backup_menu")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

# Register backup handlers
def register_backup_handlers(application):
    """Register all backup-related handlers"""
    # Command handlers
    application.add_handler(CommandHandler("backup", backup_menu_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(
        backup_callback_handler, 
        pattern=r"^backup_"
    ))
    
    logger.info("Backup handlers registered successfully")
