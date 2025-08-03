"""
Automated Backup Scheduler for PMO Recovery Bot
Handles scheduled backups and monitoring
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading

from .backup_service import backup_service
from ..utils.logger import get_logger

logger = get_logger(__name__)

class BackupScheduler:
    """Handles automated backup scheduling and monitoring"""
    
    def __init__(self):
        self.is_running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.backup_stats = {
            "last_daily_backup": None,
            "last_weekly_backup": None,
            "successful_backups": 0,
            "failed_backups": 0,
            "total_backup_size_mb": 0
        }
    
    def start_scheduler(self) -> None:
        """Start the backup scheduler"""
        if self.is_running:
            logger.warning("Backup scheduler is already running")
            return
        
        self.is_running = True
        
        # Schedule daily backups at 3 AM
        schedule.every().day.at("03:00").do(self._run_daily_backup)
        
        # Schedule weekly backups on Sunday at 2 AM
        schedule.every().sunday.at("02:00").do(self._run_weekly_backup)
        
        # Schedule backup monitoring every hour
        schedule.every().hour.do(self._monitor_backup_health)
        
        # Start scheduler in separate thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Backup scheduler started successfully")
    
    def stop_scheduler(self) -> None:
        """Stop the backup scheduler"""
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        logger.info("Backup scheduler stopped")
    
    def _run_scheduler(self) -> None:
        """Run the scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
    
    def _run_daily_backup(self) -> None:
        """Execute daily backup"""
        asyncio.create_task(self._perform_backup("daily"))
    
    def _run_weekly_backup(self) -> None:
        """Execute weekly backup"""
        asyncio.create_task(self._perform_backup("weekly"))
    
    async def _perform_backup(self, backup_type: str) -> None:
        """Perform backup and update statistics"""
        try:
            logger.info(f"Starting scheduled {backup_type} backup")
            
            success, result = await backup_service.create_full_backup(backup_type)
            
            if success:
                self.backup_stats["successful_backups"] += 1
                self.backup_stats[f"last_{backup_type}_backup"] = datetime.now().isoformat()
                logger.info(f"Scheduled {backup_type} backup completed: {result}")
            else:
                self.backup_stats["failed_backups"] += 1
                logger.error(f"Scheduled {backup_type} backup failed: {result}")
                
                # Create emergency notification for failed backup
                await self._notify_backup_failure(backup_type, result)
        
        except Exception as e:
            self.backup_stats["failed_backups"] += 1
            error_msg = f"Scheduled {backup_type} backup error: {str(e)}"
            logger.error(error_msg)
            await self._notify_backup_failure(backup_type, error_msg)
    
    async def _monitor_backup_health(self) -> None:
        """Monitor backup system health"""
        try:
            status = await backup_service.get_backup_status()
            
            # Update total backup size
            self.backup_stats["total_backup_size_mb"] = status.get("backup_directory_size_mb", 0)
            
            # Check if daily backup is overdue
            if self._is_daily_backup_overdue():
                logger.warning("Daily backup is overdue")
                await self._perform_backup("daily")
            
            # Check database integrity
            if not status.get("database_integrity", False):
                logger.error("Database integrity check failed during monitoring")
                # Create emergency backup immediately
                await self._perform_backup("emergency")
            
            # Log backup health status
            logger.debug(f"Backup health check completed: {self.backup_stats}")
            
        except Exception as e:
            logger.error(f"Backup health monitoring error: {e}")
    
    def _is_daily_backup_overdue(self) -> bool:
        """Check if daily backup is overdue (more than 25 hours since last backup)"""
        last_backup = self.backup_stats.get("last_daily_backup")
        if not last_backup:
            return True
        
        last_backup_time = datetime.fromisoformat(last_backup)
        return datetime.now() - last_backup_time > timedelta(hours=25)
    
    async def _notify_backup_failure(self, backup_type: str, error_message: str) -> None:
        """Handle backup failure notifications"""
        # This could be extended to send notifications to admins
        logger.critical(f"BACKUP FAILURE - {backup_type.upper()}: {error_message}")
        
        # You could add code here to:
        # - Send notification to admin via Telegram
        # - Send email alerts
        # - Create system alerts
        # - Trigger emergency protocols
    
    def get_backup_statistics(self) -> Dict:
        """Get current backup statistics"""
        return {
            "scheduler_running": self.is_running,
            "backup_stats": self.backup_stats.copy(),
            "next_daily_backup": self._get_next_scheduled_time("daily"),
            "next_weekly_backup": self._get_next_scheduled_time("weekly")
        }
    
    def _get_next_scheduled_time(self, backup_type: str) -> Optional[str]:
        """Get next scheduled backup time"""
        for job in schedule.jobs:
            if backup_type in str(job.job_func):
                return str(job.next_run)
        return None
    
    async def force_backup(self, backup_type: str = "manual") -> tuple[bool, str]:
        """Force an immediate backup"""
        logger.info(f"Force backup requested: {backup_type}")
        return await backup_service.create_full_backup(backup_type)

# Global backup scheduler instance
backup_scheduler = BackupScheduler()
