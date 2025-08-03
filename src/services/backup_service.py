"""
Backup and Restore Service for PMO Recovery Bot
Provides comprehensive data backup and recovery functionality
"""

import os
import json
import sqlite3
import shutil
import zipfile
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import asyncio

from ..utils.logger import app_logger

logger = app_logger

class BackupService:
    """Service for handling data backup and restore operations"""
    
    def __init__(self, db_path: str = "data/pmo_recovery.db"):
        self.db_path = db_path
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different backup types
        (self.backup_dir / "daily").mkdir(exist_ok=True)
        (self.backup_dir / "weekly").mkdir(exist_ok=True)
        (self.backup_dir / "manual").mkdir(exist_ok=True)
        (self.backup_dir / "emergency").mkdir(exist_ok=True)
    
    async def create_full_backup(self, backup_type: str = "manual") -> Tuple[bool, str]:
        """
        Create a complete backup of all bot data
        
        Args:
            backup_type: Type of backup (daily, weekly, manual, emergency)
            
        Returns:
            Tuple of (success, backup_path or error_message)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"pmo_recovery_backup_{backup_type}_{timestamp}"
            backup_path = self.backup_dir / backup_type / f"{backup_name}.zip"
            
            logger.info(f"Starting {backup_type} backup: {backup_name}")
            
            # Create temporary directory for backup files
            temp_dir = Path(f"temp_backup_{timestamp}")
            temp_dir.mkdir(exist_ok=True)
            
            try:
                # 1. Backup database
                await self._backup_database(temp_dir)
                
                # 2. Backup configuration files
                await self._backup_config_files(temp_dir)
                
                # 3. Backup data files (quotes, tips)
                await self._backup_data_files(temp_dir)
                
                # 4. Backup logs (last 30 days)
                await self._backup_recent_logs(temp_dir)
                
                # 5. Create backup metadata
                await self._create_backup_metadata(temp_dir, backup_type)
                
                # 6. Create ZIP archive
                await self._create_zip_archive(temp_dir, backup_path)
                
                # 7. Cleanup temporary directory
                shutil.rmtree(temp_dir)
                
                # 8. Cleanup old backups
                await self._cleanup_old_backups(backup_type)
                
                logger.info(f"Backup completed successfully: {backup_path}")
                return True, str(backup_path)
                
            except Exception as e:
                # Cleanup on error
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                raise e
                
        except Exception as e:
            error_msg = f"Backup failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    async def _backup_database(self, temp_dir: Path) -> None:
        """Backup the SQLite database with integrity check"""
        if not os.path.exists(self.db_path):
            logger.warning("Database file not found, skipping database backup")
            return
        
        # Check database integrity before backup
        if not await self._check_database_integrity():
            raise Exception("Database integrity check failed")
        
        # Create database backup
        db_backup_path = temp_dir / "database"
        db_backup_path.mkdir(exist_ok=True)
        
        # Copy main database
        shutil.copy2(self.db_path, db_backup_path / "pmo_recovery.db")
        
        # Export database to SQL format for additional safety
        await self._export_database_to_sql(db_backup_path / "pmo_recovery_export.sql")
        
        # Export user data to JSON for human-readable backup
        await self._export_user_data_to_json(db_backup_path / "user_data_export.json")
        
        logger.info("Database backup completed")
    
    async def _backup_config_files(self, temp_dir: Path) -> None:
        """Backup configuration files"""
        config_backup_path = temp_dir / "config"
        config_backup_path.mkdir(exist_ok=True)
        
        config_files = [
            "config/settings.py",
            "requirements.txt",
            "requirements-dev.txt"
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                shutil.copy2(config_file, config_backup_path / os.path.basename(config_file))
        
        logger.info("Configuration files backup completed")
    
    async def _backup_data_files(self, temp_dir: Path) -> None:
        """Backup data files (quotes, tips, etc.)"""
        data_backup_path = temp_dir / "data"
        data_backup_path.mkdir(exist_ok=True)
        
        data_files = [
            "data/quotes.json",
            "data/tips.json"
        ]
        
        for data_file in data_files:
            if os.path.exists(data_file):
                shutil.copy2(data_file, data_backup_path / os.path.basename(data_file))
        
        logger.info("Data files backup completed")
    
    async def _backup_recent_logs(self, temp_dir: Path) -> None:
        """Backup recent log files (last 30 days)"""
        logs_backup_path = temp_dir / "logs"
        logs_backup_path.mkdir(exist_ok=True)
        
        logs_dir = Path("logs")
        if not logs_dir.exists():
            return
        
        # Get log files from last 30 days
        thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        
        for log_file in logs_dir.glob("*.log"):
            if log_file.stat().st_mtime > thirty_days_ago:
                shutil.copy2(log_file, logs_backup_path / log_file.name)
        
        logger.info("Recent logs backup completed")
    
    async def _create_backup_metadata(self, temp_dir: Path, backup_type: str) -> None:
        """Create backup metadata file"""
        metadata = {
            "backup_type": backup_type,
            "created_at": datetime.now().isoformat(),
            "bot_version": "1.0.0",  # You can make this dynamic
            "database_path": self.db_path,
            "files_included": [],
            "user_count": await self._get_user_count(),
            "journal_entries_count": await self._get_journal_entries_count(),
            "database_size_mb": self._get_file_size_mb(self.db_path) if os.path.exists(self.db_path) else 0
        }
        
        # List all files included in backup
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_dir)
                metadata["files_included"].append(relative_path)
        
        metadata_file = temp_dir / "backup_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info("Backup metadata created")
    
    async def _create_zip_archive(self, temp_dir: Path, backup_path: Path) -> None:
        """Create ZIP archive from temporary directory"""
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arc_name)
        
        logger.info(f"ZIP archive created: {backup_path}")
    
    async def _cleanup_old_backups(self, backup_type: str) -> None:
        """Remove old backups based on retention policy"""
        backup_folder = self.backup_dir / backup_type
        
        # Retention policy
        retention_days = {
            "daily": 7,      # Keep 7 daily backups
            "weekly": 4,     # Keep 4 weekly backups
            "manual": 10,    # Keep 10 manual backups
            "emergency": 3   # Keep 3 emergency backups
        }
        
        days_to_keep = retention_days.get(backup_type, 7)
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        for backup_file in backup_folder.glob("*.zip"):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")
    
    async def restore_from_backup(self, backup_path: str, confirm_restore: bool = False) -> Tuple[bool, str]:
        """
        Restore data from a backup file
        
        Args:
            backup_path: Path to the backup ZIP file
            confirm_restore: Safety confirmation flag
            
        Returns:
            Tuple of (success, message)
        """
        if not confirm_restore:
            return False, "Restore operation requires explicit confirmation (confirm_restore=True)"
        
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return False, f"Backup file not found: {backup_path}"
            
            logger.info(f"Starting restore from backup: {backup_path}")
            
            # Create emergency backup before restore
            emergency_backup_result = await self.create_full_backup("emergency")
            if not emergency_backup_result[0]:
                return False, f"Failed to create emergency backup before restore: {emergency_backup_result[1]}"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            restore_temp_dir = Path(f"temp_restore_{timestamp}")
            
            try:
                # Extract backup
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    zipf.extractall(restore_temp_dir)
                
                # Read backup metadata
                metadata_file = restore_temp_dir / "backup_metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    logger.info(f"Restoring backup from {metadata['created_at']}")
                
                # Restore database
                await self._restore_database(restore_temp_dir)
                
                # Restore configuration files
                await self._restore_config_files(restore_temp_dir)
                
                # Restore data files
                await self._restore_data_files(restore_temp_dir)
                
                # Cleanup temporary directory
                shutil.rmtree(restore_temp_dir)
                
                success_msg = f"Restore completed successfully from {backup_path}"
                logger.info(success_msg)
                return True, success_msg
                
            except Exception as e:
                # Cleanup on error
                if restore_temp_dir.exists():
                    shutil.rmtree(restore_temp_dir)
                raise e
                
        except Exception as e:
            error_msg = f"Restore failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    async def _restore_database(self, restore_dir: Path) -> None:
        """Restore database from backup"""
        db_restore_path = restore_dir / "database" / "pmo_recovery.db"
        
        if not db_restore_path.exists():
            raise Exception("Database backup not found in restore directory")
        
        # Create backup of current database
        if os.path.exists(self.db_path):
            current_db_backup = f"{self.db_path}.pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(self.db_path, current_db_backup)
            logger.info(f"Current database backed up to: {current_db_backup}")
        
        # Restore database
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        shutil.copy2(db_restore_path, self.db_path)
        
        # Verify restored database integrity
        if not await self._check_database_integrity():
            raise Exception("Restored database failed integrity check")
        
        logger.info("Database restore completed")
    
    async def _restore_config_files(self, restore_dir: Path) -> None:
        """Restore configuration files from backup"""
        config_restore_path = restore_dir / "config"
        
        if not config_restore_path.exists():
            logger.warning("Configuration files not found in backup")
            return
        
        for config_file in config_restore_path.glob("*"):
            if config_file.name == "settings.py":
                # Special handling for settings.py
                target_path = "config/settings.py"
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(config_file, target_path)
            else:
                # Other config files go to root
                shutil.copy2(config_file, config_file.name)
        
        logger.info("Configuration files restore completed")
    
    async def _restore_data_files(self, restore_dir: Path) -> None:
        """Restore data files from backup"""
        data_restore_path = restore_dir / "data"
        
        if not data_restore_path.exists():
            logger.warning("Data files not found in backup")
            return
        
        os.makedirs("data", exist_ok=True)
        
        for data_file in data_restore_path.glob("*"):
            if data_file.name.endswith(('.json', '.txt')):
                shutil.copy2(data_file, f"data/{data_file.name}")
        
        logger.info("Data files restore completed")
    
    async def list_available_backups(self) -> Dict[str, List[Dict]]:
        """List all available backups by type"""
        backups = {
            "daily": [],
            "weekly": [],
            "manual": [],
            "emergency": []
        }
        
        for backup_type in backups.keys():
            backup_folder = self.backup_dir / backup_type
            if backup_folder.exists():
                for backup_file in backup_folder.glob("*.zip"):
                    backup_info = {
                        "filename": backup_file.name,
                        "path": str(backup_file),
                        "size_mb": self._get_file_size_mb(str(backup_file)),
                        "created_at": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat(),
                        "age_days": (datetime.now().timestamp() - backup_file.stat().st_mtime) / (24 * 60 * 60)
                    }
                    
                    # Try to read metadata if available
                    try:
                        with zipfile.ZipFile(backup_file, 'r') as zipf:
                            if 'backup_metadata.json' in zipf.namelist():
                                with zipf.open('backup_metadata.json') as f:
                                    metadata = json.load(f)
                                    backup_info.update({
                                        "user_count": metadata.get("user_count"),
                                        "journal_entries_count": metadata.get("journal_entries_count"),
                                        "bot_version": metadata.get("bot_version")
                                    })
                    except Exception as e:
                        logger.warning(f"Could not read metadata from {backup_file}: {e}")
                    
                    backups[backup_type].append(backup_info)
                
                # Sort by creation time (newest first)
                backups[backup_type].sort(key=lambda x: x["created_at"], reverse=True)
        
        return backups
    
    async def get_backup_status(self) -> Dict:
        """Get current backup system status"""
        status = {
            "backup_directory": str(self.backup_dir),
            "database_path": self.db_path,
            "database_exists": os.path.exists(self.db_path),
            "database_size_mb": self._get_file_size_mb(self.db_path) if os.path.exists(self.db_path) else 0,
            "database_integrity": await self._check_database_integrity(),
            "total_backups": 0,
            "latest_backup": None,
            "backup_directory_size_mb": 0
        }
        
        # Count total backups and find latest
        latest_backup_time = 0
        latest_backup_info = None
        
        for backup_type in ["daily", "weekly", "manual", "emergency"]:
            backup_folder = self.backup_dir / backup_type
            if backup_folder.exists():
                for backup_file in backup_folder.glob("*.zip"):
                    status["total_backups"] += 1
                    status["backup_directory_size_mb"] += self._get_file_size_mb(str(backup_file))
                    
                    file_time = backup_file.stat().st_mtime
                    if file_time > latest_backup_time:
                        latest_backup_time = file_time
                        latest_backup_info = {
                            "filename": backup_file.name,
                            "type": backup_type,
                            "created_at": datetime.fromtimestamp(file_time).isoformat(),
                            "size_mb": self._get_file_size_mb(str(backup_file))
                        }
        
        if latest_backup_info:
            status["latest_backup"] = latest_backup_info
        
        return status
    
    # Helper methods
    async def _check_database_integrity(self) -> bool:
        """Check SQLite database integrity"""
        if not os.path.exists(self.db_path):
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            return result[0] == "ok"
        except Exception as e:
            logger.error(f"Database integrity check failed: {e}")
            return False
    
    async def _export_database_to_sql(self, output_path: str) -> None:
        """Export database to SQL format"""
        if not os.path.exists(self.db_path):
            return
        
        conn = sqlite3.connect(self.db_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()
    
    async def _export_user_data_to_json(self, output_path: str) -> None:
        """Export user data to JSON format for human-readable backup"""
        if not os.path.exists(self.db_path):
            return
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        export_data = {
            "users": [],
            "journal_entries": [],
            "user_settings": [],
            "streaks": []
        }
        
        # Export users
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            export_data["users"].append(dict(row))
        
        # Export journal entries
        cursor.execute("SELECT * FROM journal_entries")
        for row in cursor.fetchall():
            export_data["journal_entries"].append(dict(row))
        
        # Export user settings if table exists
        try:
            cursor.execute("SELECT * FROM user_settings")
            for row in cursor.fetchall():
                export_data["user_settings"].append(dict(row))
        except sqlite3.OperationalError:
            pass  # Table doesn't exist
        
        # Export streaks if table exists
        try:
            cursor.execute("SELECT * FROM streaks")
            for row in cursor.fetchall():
                export_data["streaks"].append(dict(row))
        except sqlite3.OperationalError:
            pass  # Table doesn't exist
        
        conn.close()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
    
    async def _get_user_count(self) -> int:
        """Get total number of users"""
        if not os.path.exists(self.db_path):
            return 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0
    
    async def _get_journal_entries_count(self) -> int:
        """Get total number of journal entries"""
        if not os.path.exists(self.db_path):
            return 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM journal_entries")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0
    
    def _get_file_size_mb(self, file_path: str) -> float:
        """Get file size in MB"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except Exception:
            return 0.0

# Global backup service instance
backup_service = BackupService()
