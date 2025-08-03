"""
Data Recovery and Restore Utilities for PMO Recovery Bot
Advanced tools for data recovery and system repair
"""

import os
import json
import sqlite3
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import zipfile

from ..utils.logger import get_logger

logger = get_logger(__name__)

class DataRecoveryTool:
    """Advanced data recovery and repair utilities"""
    
    def __init__(self, db_path: str = "data/pmo_recovery.db"):
        self.db_path = db_path
        self.recovery_dir = Path("recovery")
        self.recovery_dir.mkdir(exist_ok=True)
    
    async def diagnose_database_issues(self) -> Dict[str, Any]:
        """Comprehensive database diagnosis"""
        diagnosis = {
            "database_exists": False,
            "database_accessible": False,
            "integrity_check": False,
            "table_structure": {},
            "data_consistency": {},
            "corruption_indicators": [],
            "repair_recommendations": [],
            "backup_suggestions": []
        }
        
        try:
            # Check if database file exists
            diagnosis["database_exists"] = os.path.exists(self.db_path)
            
            if not diagnosis["database_exists"]:
                diagnosis["corruption_indicators"].append("Database file missing")
                diagnosis["repair_recommendations"].append("Restore from latest backup")
                diagnosis["backup_suggestions"].append("Check backup directory for available backups")
                return diagnosis
            
            # Check database accessibility
            try:
                conn = sqlite3.connect(self.db_path)
                diagnosis["database_accessible"] = True
                
                # Run integrity check
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                diagnosis["integrity_check"] = result[0] == "ok"
                
                if not diagnosis["integrity_check"]:
                    diagnosis["corruption_indicators"].append(f"Integrity check failed: {result[0]}")
                
                # Check table structure
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    diagnosis["table_structure"][table_name] = [
                        {
                            "name": col[1],
                            "type": col[2],
                            "notnull": bool(col[3]),
                            "pk": bool(col[5])
                        } for col in columns
                    ]
                
                # Check data consistency
                await self._check_data_consistency(cursor, diagnosis)
                
                conn.close()
                
            except sqlite3.DatabaseError as e:
                diagnosis["corruption_indicators"].append(f"Database error: {str(e)}")
                diagnosis["repair_recommendations"].append("Database may be corrupted - restore from backup")
            
            # Generate repair recommendations
            await self._generate_repair_recommendations(diagnosis)
            
        except Exception as e:
            logger.error(f"Database diagnosis error: {e}")
            diagnosis["corruption_indicators"].append(f"Diagnosis error: {str(e)}")
        
        return diagnosis
    
    async def _check_data_consistency(self, cursor: sqlite3.Cursor, diagnosis: Dict) -> None:
        """Check data consistency across tables"""
        consistency_checks = {}
        
        try:
            # Check users table
            if "users" in diagnosis["table_structure"]:
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM users")
                unique_users = cursor.fetchone()[0]
                
                consistency_checks["users"] = {
                    "total_records": user_count,
                    "unique_users": unique_users,
                    "duplicates": user_count - unique_users
                }
                
                if user_count != unique_users:
                    diagnosis["corruption_indicators"].append(f"Duplicate users detected: {user_count - unique_users}")
            
            # Check journal entries
            if "journal_entries" in diagnosis["table_structure"]:
                cursor.execute("SELECT COUNT(*) FROM journal_entries")
                journal_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM journal_entries WHERE content IS NOT NULL AND content != ''")
                valid_entries = cursor.fetchone()[0]
                
                consistency_checks["journal_entries"] = {
                    "total_entries": journal_count,
                    "valid_entries": valid_entries,
                    "empty_entries": journal_count - valid_entries
                }
            
            # Check foreign key relationships
            cursor.execute("PRAGMA foreign_key_check")
            fk_violations = cursor.fetchall()
            if fk_violations:
                diagnosis["corruption_indicators"].append(f"Foreign key violations: {len(fk_violations)}")
                consistency_checks["foreign_key_violations"] = len(fk_violations)
            
            diagnosis["data_consistency"] = consistency_checks
            
        except Exception as e:
            logger.error(f"Data consistency check error: {e}")
            diagnosis["corruption_indicators"].append(f"Consistency check error: {str(e)}")
    
    async def _generate_repair_recommendations(self, diagnosis: Dict) -> None:
        """Generate repair recommendations based on diagnosis"""
        recommendations = []
        
        if not diagnosis["database_exists"]:
            recommendations.extend([
                "1. Check if database file was moved or deleted",
                "2. Restore from latest backup immediately",
                "3. Check backup directory for available backups"
            ])
        
        elif not diagnosis["database_accessible"]:
            recommendations.extend([
                "1. Check file permissions on database",
                "2. Verify disk space availability",
                "3. Consider restoring from backup"
            ])
        
        elif not diagnosis["integrity_check"]:
            recommendations.extend([
                "1. Create emergency backup before repair attempts",
                "2. Try SQLite .recover command",
                "3. Restore from clean backup if repair fails"
            ])
        
        if diagnosis["corruption_indicators"]:
            recommendations.append("4. Run full system backup after successful repair")
        
        # Check for missing critical tables
        required_tables = ["users", "journal_entries"]
        existing_tables = list(diagnosis["table_structure"].keys())
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            recommendations.append(f"5. Recreate missing tables: {', '.join(missing_tables)}")
        
        diagnosis["repair_recommendations"] = recommendations
    
    async def attempt_database_repair(self, create_backup: bool = True) -> Tuple[bool, str]:
        """Attempt to repair database corruption"""
        if create_backup:
            # Create backup before repair
            backup_path = self.recovery_dir / f"pre_repair_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_path)
                logger.info(f"Pre-repair backup created: {backup_path}")
        
        try:
            # Method 1: SQLite .recover
            recovered_db_path = await self._recover_with_sqlite_recover()
            if recovered_db_path:
                return True, f"Database recovered successfully: {recovered_db_path}"
            
            # Method 2: Export and reimport
            export_success = await self._export_recoverable_data()
            if export_success:
                return True, "Data exported successfully - manual import required"
            
            return False, "All repair methods failed"
            
        except Exception as e:
            error_msg = f"Database repair failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    async def _recover_with_sqlite_recover(self) -> Optional[str]:
        """Use SQLite .recover command to recover data"""
        try:
            recovery_db_path = self.recovery_dir / f"recovered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            # Create recovery database
            recovery_conn = sqlite3.connect(str(recovery_db_path))
            recovery_cursor = recovery_conn.cursor()
            
            # Try to copy recoverable data
            original_conn = sqlite3.connect(self.db_path)
            
            # Get table schemas
            original_cursor = original_conn.cursor()
            original_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
            table_schemas = original_cursor.fetchall()
            
            # Recreate table structure in recovery database
            for schema in table_schemas:
                if schema[0]:  # Skip None schemas
                    recovery_cursor.execute(schema[0])
            
            # Copy data table by table
            original_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = original_cursor.fetchall()
            
            recovered_tables = []
            for table in tables:
                table_name = table[0]
                try:
                    original_cursor.execute(f"SELECT * FROM {table_name}")
                    rows = original_cursor.fetchall()
                    
                    if rows:
                        # Get column count
                        original_cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = original_cursor.fetchall()
                        placeholders = ",".join(["?" for _ in columns])
                        
                        recovery_cursor.executemany(
                            f"INSERT INTO {table_name} VALUES ({placeholders})",
                            rows
                        )
                        recovered_tables.append(table_name)
                
                except sqlite3.Error as e:
                    logger.warning(f"Could not recover table {table_name}: {e}")
            
            recovery_conn.commit()
            recovery_conn.close()
            original_conn.close()
            
            if recovered_tables:
                logger.info(f"Recovered tables: {recovered_tables}")
                return str(recovery_db_path)
            
        except Exception as e:
            logger.error(f"SQLite recover method failed: {e}")
        
        return None
    
    async def _export_recoverable_data(self) -> bool:
        """Export recoverable data to JSON files"""
        try:
            export_dir = self.recovery_dir / f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            export_dir.mkdir(exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            exported_tables = []
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # Convert to JSON-serializable format
                        data = []
                        for row in rows:
                            row_data = {}
                            for key in row.keys():
                                value = row[key]
                                # Handle datetime conversion
                                if isinstance(value, str) and "T" in value:
                                    row_data[key] = value
                                else:
                                    row_data[key] = value
                            data.append(row_data)
                        
                        # Save to JSON file
                        export_file = export_dir / f"{table_name}.json"
                        with open(export_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                        
                        exported_tables.append(table_name)
                        logger.info(f"Exported {len(data)} records from {table_name}")
                
                except sqlite3.Error as e:
                    logger.warning(f"Could not export table {table_name}: {e}")
            
            conn.close()
            
            # Create export summary
            summary = {
                "export_date": datetime.now().isoformat(),
                "exported_tables": exported_tables,
                "export_directory": str(export_dir)
            }
            
            summary_file = export_dir / "export_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            return len(exported_tables) > 0
            
        except Exception as e:
            logger.error(f"Data export failed: {e}")
            return False
    
    async def rebuild_database_from_backup(self, backup_path: str) -> Tuple[bool, str]:
        """Rebuild database from backup with data validation"""
        try:
            if not os.path.exists(backup_path):
                return False, f"Backup file not found: {backup_path}"
            
            # Create current database backup
            if os.path.exists(self.db_path):
                backup_current = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(self.db_path, backup_current)
                logger.info(f"Current database backed up to: {backup_current}")
            
            # Extract and validate backup
            temp_extract_dir = self.recovery_dir / f"temp_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_extract_dir)
            
            # Find database file in backup
            backup_db_path = temp_extract_dir / "database" / "pmo_recovery.db"
            if not backup_db_path.exists():
                return False, "Database file not found in backup"
            
            # Validate backup database
            validation_result = await self._validate_backup_database(str(backup_db_path))
            if not validation_result[0]:
                return False, f"Backup validation failed: {validation_result[1]}"
            
            # Replace current database
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            shutil.copy2(backup_db_path, self.db_path)
            
            # Cleanup
            shutil.rmtree(temp_extract_dir)
            
            success_msg = f"Database successfully rebuilt from backup: {backup_path}"
            logger.info(success_msg)
            return True, success_msg
            
        except Exception as e:
            error_msg = f"Database rebuild failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    async def _validate_backup_database(self, db_path: str) -> Tuple[bool, str]:
        """Validate backup database integrity and structure"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check integrity
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] != "ok":
                conn.close()
                return False, f"Integrity check failed: {result[0]}"
            
            # Check required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            
            required_tables = ["users", "journal_entries"]
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                conn.close()
                return False, f"Missing required tables: {missing_tables}"
            
            # Check data exists
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            conn.close()
            
            return True, f"Backup validated successfully ({user_count} users found)"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    async def create_recovery_report(self) -> str:
        """Create comprehensive recovery report"""
        report_data = {
            "report_date": datetime.now().isoformat(),
            "database_diagnosis": await self.diagnose_database_issues(),
            "system_info": await self._get_system_info(),
            "recovery_options": await self._get_recovery_options()
        }
        
        report_file = self.recovery_dir / f"recovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Recovery report created: {report_file}")
        return str(report_file)
    
    async def _get_system_info(self) -> Dict:
        """Get system information for recovery report"""
        info = {
            "database_path": self.db_path,
            "database_size_mb": 0,
            "recovery_directory": str(self.recovery_dir),
            "available_backups": 0,
            "disk_space_available": True
        }
        
        try:
            if os.path.exists(self.db_path):
                info["database_size_mb"] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            # Count available backups
            backup_dir = Path("backups")
            if backup_dir.exists():
                backup_count = 0
                for backup_type_dir in backup_dir.iterdir():
                    if backup_type_dir.is_dir():
                        backup_count += len(list(backup_type_dir.glob("*.zip")))
                info["available_backups"] = backup_count
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
        
        return info
    
    async def _get_recovery_options(self) -> List[Dict]:
        """Get available recovery options"""
        options = []
        
        # Check for recent backups
        backup_dir = Path("backups")
        if backup_dir.exists():
            for backup_type in ["emergency", "daily", "weekly", "manual"]:
                type_dir = backup_dir / backup_type
                if type_dir.exists():
                    backups = list(type_dir.glob("*.zip"))
                    if backups:
                        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
                        age_hours = (datetime.now().timestamp() - latest_backup.stat().st_mtime) / 3600
                        
                        options.append({
                            "type": f"restore_from_{backup_type}",
                            "description": f"Restore from {backup_type} backup",
                            "file": str(latest_backup),
                            "age_hours": age_hours,
                            "recommended": age_hours < 24
                        })
        
        # Always available options
        options.extend([
            {
                "type": "database_repair",
                "description": "Attempt database repair",
                "recommended": True
            },
            {
                "type": "data_export",
                "description": "Export recoverable data",
                "recommended": False
            },
            {
                "type": "fresh_start",
                "description": "Initialize fresh database",
                "recommended": False
            }
        ])
        
        return options

# Global recovery tool instance
recovery_tool = DataRecoveryTool()
