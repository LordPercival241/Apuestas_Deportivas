"""
System Configuration Management
Handles environment variables, API keys, and system parameters
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    # Project paths
    BASE_DIR = Path(__file__).parent
    LOG_DIR = BASE_DIR / "logs"
    
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "sports_betting_db")
    DB_USER = os.getenv("DB_USER", "betting_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    
    # API Keys
    SPORTRADAR_API_KEY = os.getenv("SPORTRADAR_API_KEY")
    BETFAIR_USERNAME = os.getenv("BETFAIR_USERNAME")
    BETFAIR_PASSWORD = os.getenv("BETFAIR_PASSWORD")
    BETFAIR_APP_KEY = os.getenv("BETFAIR_APP_KEY")
    
    # System
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Risk Management Thresholds
    MAX_DAILY_LOSS_PERCENT = float(os.getenv("MAX_DAILY_LOSS_PERCENT", 5.0))
    MAX_SINGLE_BET_PERCENT = float(os.getenv("MAX_SINGLE_BET_PERCENT", 2.0))
    MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", 0.60))
    BANKROLL_INITIAL = float(os.getenv("BANKROLL_INITIAL", 1000.00))
    
    # Responsible Gaming
    PAUSE_AFTER_LOSS_STREAK = int(os.getenv("PAUSE_AFTER_LOSS_STREAK", 3))
    MAX_BETS_PER_DAY = int(os.getenv("MAX_BETS_PER_DAY", 20))
    GEOLOCATION_CHECK = os.getenv("GEOLOCATION_CHECK", "True").lower() == "true"
    AGE_VERIFICATION_REQUIRED = os.getenv("AGE_VERIFICATION_REQUIRED", "True").lower() == "true"
    
    # Execution Mode
    PAPER_TRADING = os.getenv("PAPER_TRADING", "True").lower() == "true"
    LIVE_TRADING = os.getenv("LIVE_TRADING", "False").lower() == "true"
    MIN_ODDS = float(os.getenv("MIN_ODDS", 1.50))
    MAX_ODDS = float(os.getenv("MAX_ODDS", 10.0))
    
    # Compliance
    REGION = os.getenv("REGION", "EU")
    REGULATORY_FRAMEWORK = os.getenv("REGULATORY_FRAMEWORK", "GDPR")
    AUDIT_LOGGING = os.getenv("AUDIT_LOGGING", "True").lower() == "true"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    PAPER_TRADING = True
    LIVE_TRADING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    PAPER_TRADING = False
    LIVE_TRADING = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DB_NAME = "sports_betting_test_db"
    PAPER_TRADING = True
    LIVE_TRADING = False

# Select configuration based on environment
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

current_config = config.get(os.getenv("ENVIRONMENT", "development"))
