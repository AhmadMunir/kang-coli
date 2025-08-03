#!/usr/bin/env python3
"""
Automated Backup Script for PMO Recovery Bot
Can be run as standalone script or scheduled via cron/task scheduler
"""

import os
import sys
import asyncio
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.backup_service import backup_service
from src.services.backup_scheduler import backup_scheduler
from src.utils.recovery_tool import recovery_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def create_backup(backup_type: str = "manual") -> None:
    """Create a backup of the specified type"""
    print(f"🔄 Creating {backup_type} backup...")
    
    try:
        success, result = await backup_service.create_full_backup(backup_type)
        
        if success:
            print(f"✅ Backup created successfully!")
            print(f"📁 Location: {result}")
            
            # Get backup info
            backup_path = Path(result)
            file_size_mb = backup_path.stat().st_size / (1024 * 1024)
            print(f"📊 Size: {file_size_mb:.2f} MB")
            print(f"⏰ Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ Backup failed: {result}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Backup error: {str(e)}")
        sys.exit(1)

async def list_backups() -> None:
    """List all available backups"""
    print("📋 Listing available backups...\n")
    
    try:
        backups = await backup_service.list_available_backups()
        
        total_backups = 0
        total_size_mb = 0
        
        for backup_type, backup_list in backups.items():
            if backup_list:
                print(f"📂 {backup_type.upper()} BACKUPS:")
                for backup in backup_list:
                    age_days = int(backup['age_days'])
                    age_text = f"{age_days}d ago" if age_days > 0 else "Today"
                    
                    print(f"  • {backup['filename']}")
                    print(f"    Size: {backup['size_mb']:.2f} MB | Age: {age_text}")
                    print(f"    Created: {backup['created_at'][:19].replace('T', ' ')}")
                    
                    if 'user_count' in backup:
                        print(f"    Users: {backup['user_count']} | Entries: {backup.get('journal_entries_count', 'N/A')}")
                    print()
                    
                    total_backups += 1
                    total_size_mb += backup['size_mb']
                print()
        
        if total_backups == 0:
            print("📭 No backups found.")
        else:
            print(f"📊 SUMMARY:")
            print(f"Total backups: {total_backups}")
            print(f"Total size: {total_size_mb:.2f} MB")
            
    except Exception as e:
        print(f"❌ Error listing backups: {str(e)}")
        sys.exit(1)

async def show_status() -> None:
    """Show backup system status"""
    print("📊 Backup System Status\n")
    
    try:
        # Get backup service status
        status = await backup_service.get_backup_status()
        
        print(f"🗄️ DATABASE:")
        print(f"  Path: {status['database_path']}")
        print(f"  Exists: {'✅ Yes' if status['database_exists'] else '❌ No'}")
        print(f"  Size: {status['database_size_mb']:.2f} MB")
        print(f"  Integrity: {'✅ OK' if status['database_integrity'] else '❌ Issues'}")
        print()
        
        print(f"💾 BACKUPS:")
        print(f"  Total backups: {status['total_backups']}")
        print(f"  Storage used: {status['backup_directory_size_mb']:.2f} MB")
        print()
        
        if status['latest_backup']:
            latest = status['latest_backup']
            print(f"🕒 LATEST BACKUP:")
            print(f"  Type: {latest['type'].capitalize()}")
            print(f"  Created: {latest['created_at'][:19].replace('T', ' ')}")
            print(f"  Size: {latest['size_mb']:.2f} MB")
            print()
        
        # Get scheduler status
        scheduler_stats = backup_scheduler.get_backup_statistics()
        
        print(f"⚙️ SCHEDULER:")
        print(f"  Status: {'🟢 Running' if scheduler_stats['scheduler_running'] else '🔴 Stopped'}")
        print(f"  Successful backups: {scheduler_stats['backup_stats']['successful_backups']}")
        print(f"  Failed backups: {scheduler_stats['backup_stats']['failed_backups']}")
        
        if scheduler_stats['next_daily_backup']:
            print(f"  Next daily backup: {scheduler_stats['next_daily_backup']}")
        print()
        
    except Exception as e:
        print(f"❌ Error getting status: {str(e)}")
        sys.exit(1)

async def diagnose_database() -> None:
    """Run database diagnosis"""
    print("🔍 Running database diagnosis...\n")
    
    try:
        diagnosis = await recovery_tool.diagnose_database_issues()
        
        print(f"📊 DIAGNOSIS RESULTS:")
        print(f"  Database exists: {'✅ Yes' if diagnosis['database_exists'] else '❌ No'}")
        print(f"  Database accessible: {'✅ Yes' if diagnosis['database_accessible'] else '❌ No'}")
        print(f"  Integrity check: {'✅ Pass' if diagnosis['integrity_check'] else '❌ Fail'}")
        print()
        
        if diagnosis['table_structure']:
            print(f"📋 TABLES FOUND:")
            for table_name, columns in diagnosis['table_structure'].items():
                print(f"  • {table_name} ({len(columns)} columns)")
            print()
        
        if diagnosis['data_consistency']:
            print(f"📈 DATA CONSISTENCY:")
            for table, stats in diagnosis['data_consistency'].items():
                print(f"  • {table}: {stats}")
            print()
        
        if diagnosis['corruption_indicators']:
            print(f"⚠️  ISSUES DETECTED:")
            for issue in diagnosis['corruption_indicators']:
                print(f"  • {issue}")
            print()
        
        if diagnosis['repair_recommendations']:
            print(f"🔧 REPAIR RECOMMENDATIONS:")
            for i, recommendation in enumerate(diagnosis['repair_recommendations'], 1):
                print(f"  {i}. {recommendation}")
            print()
        
        # Create detailed report
        report_path = await recovery_tool.create_recovery_report()
        print(f"📄 Detailed report saved to: {report_path}")
        
    except Exception as e:
        print(f"❌ Diagnosis error: {str(e)}")
        sys.exit(1)

async def restore_backup(backup_path: str, confirm: bool = False) -> None:
    """Restore from backup"""
    if not confirm:
        print("⚠️  WARNING: This will replace all current data!")
        print("Use --confirm flag if you're sure you want to proceed.")
        return
    
    print(f"🔄 Restoring from backup: {backup_path}")
    print("⏳ Please wait...")
    
    try:
        success, result = await backup_service.restore_from_backup(backup_path, confirm_restore=True)
        
        if success:
            print(f"✅ Restore completed successfully!")
            print(f"📝 {result}")
        else:
            print(f"❌ Restore failed: {result}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Restore error: {str(e)}")
        sys.exit(1)

async def start_scheduler() -> None:
    """Start the backup scheduler"""
    print("⚙️ Starting backup scheduler...")
    
    try:
        backup_scheduler.start_scheduler()
        print("✅ Backup scheduler started successfully!")
        print("📅 Schedule:")
        print("  • Daily backups: 03:00 AM")
        print("  • Weekly backups: Sunday 02:00 AM")
        print("\n🔄 Scheduler is now running in background...")
        print("Press Ctrl+C to stop")
        
        # Keep the script running
        try:
            while True:
                await asyncio.sleep(60)
                stats = backup_scheduler.get_backup_statistics()
                if not stats['scheduler_running']:
                    print("⚠️ Scheduler stopped unexpectedly")
                    break
        except KeyboardInterrupt:
            print("\n⏹️ Stopping scheduler...")
            backup_scheduler.stop_scheduler()
            print("✅ Scheduler stopped")
            
    except Exception as e:
        print(f"❌ Scheduler error: {str(e)}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="PMO Recovery Bot Backup Management")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create backup command
    backup_parser = subparsers.add_parser('backup', help='Create a backup')
    backup_parser.add_argument('--type', choices=['daily', 'weekly', 'manual', 'emergency'], 
                              default='manual', help='Backup type (default: manual)')
    
    # List backups command
    subparsers.add_parser('list', help='List available backups')
    
    # Status command
    subparsers.add_parser('status', help='Show backup system status')
    
    # Diagnose command
    subparsers.add_parser('diagnose', help='Run database diagnosis')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_path', help='Path to backup file')
    restore_parser.add_argument('--confirm', action='store_true', 
                               help='Confirm restoration (required)')
    
    # Scheduler command
    subparsers.add_parser('scheduler', help='Start backup scheduler')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Run the appropriate command
    if args.command == 'backup':
        asyncio.run(create_backup(args.type))
    elif args.command == 'list':
        asyncio.run(list_backups())
    elif args.command == 'status':
        asyncio.run(show_status())
    elif args.command == 'diagnose':
        asyncio.run(diagnose_database())
    elif args.command == 'restore':
        asyncio.run(restore_backup(args.backup_path, args.confirm))
    elif args.command == 'scheduler':
        asyncio.run(start_scheduler())

if __name__ == "__main__":
    main()
