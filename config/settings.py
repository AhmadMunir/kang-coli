import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings configuration"""
    
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "pmo_recovery_bot")
    ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/database.db")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Timezone Configuration
    TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta")
    
    # Daily reminder configuration
    DAILY_REMINDER_TIME = os.getenv("DAILY_REMINDER_TIME", "08:00")
    AFTERNOON_BOOST_TIME = os.getenv("AFTERNOON_BOOST_TIME", "15:00")
    EVENING_REFLECTION_TIME = os.getenv("EVENING_REFLECTION_TIME", "21:00")
    WEEKLY_SUMMARY_DAY = int(os.getenv("WEEKLY_SUMMARY_DAY", "6"))  # 6 = Sunday
    WEEKLY_SUMMARY_TIME = os.getenv("WEEKLY_SUMMARY_TIME", "10:00")
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required. Please set it in .env file")
        
        return True

# Create settings instance
settings = Settings()
