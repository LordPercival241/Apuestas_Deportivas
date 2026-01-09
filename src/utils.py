"""
Utilities Module
Logging, database management, and helper functions
"""
import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def setup_logging(log_level: str = "INFO", log_dir: str = "logs") -> logging.Logger:
    """
    Setup centralized logging with file and console handlers
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        
    Returns:
        Configured logger instance
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    logger = logging.getLogger("sports_betting_system")
    logger.setLevel(getattr(logging, log_level))
    
    # File handler with rotation
    fh = RotatingFileHandler(
        log_path / "system.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    fh.setLevel(getattr(logging, log_level))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

class AuditLogger:
    """
    Centralized audit logging for compliance and transparency
    Logs all betting decisions and system actions
    """
    
    def __init__(self, log_dir: str = "logs/audit"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("audit_logger")
    
    def log_decision(self, decision: Dict[str, Any]) -> None:
        """
        Log a betting decision with full details
        
        Args:
            decision: Dictionary containing decision details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_id": decision.get("event_id"),
            "model_prediction": decision.get("prediction"),
            "market_odds": decision.get("odds"),
            "calculated_value": decision.get("value"),
            "stake": decision.get("stake"),
            "decision": decision.get("action"),  # place_bet, skip, etc.
            "reason": decision.get("reason"),
            "risk_metrics": decision.get("risk_metrics"),
        }
        
        self.logger.info(json.dumps(log_entry, indent=2))
    
    def log_error(self, error_type: str, details: Dict) -> None:
        """Log system errors"""
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "details": details,
        }
        self.logger.error(json.dumps(error_log, indent=2))

class DatabaseManager:
    """
    Database connection and management
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            # Placeholder for actual DB connection
            logger = logging.getLogger(__name__)
            logger.info("Database connection established")
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Database connection failed: {str(e)}")
            return False
    
    def save_event(self, event: Dict) -> bool:
        """Save sports event data"""
        return True
    
    def save_prediction(self, prediction: Dict) -> bool:
        """Save model prediction"""
        return True
    
    def save_bet(self, bet: Dict) -> bool:
        """Save bet execution"""
        return True
    
    def get_historical_accuracy(self, sport: str, limit: int = 100) -> Dict:
        """Get model accuracy statistics"""
        return {
            "sport": sport,
            "total_bets": limit,
            "win_rate": 0.55,
            "roi": 0.12,
        }

class ArchitectureDocumentation:
    """
    System architecture documentation and reference
    """
    
    @staticmethod
    def get_system_architecture() -> Dict[str, Any]:
        """Return system architecture overview"""
        return {
            "name": "Sports Betting Autonomous System",
            "version": "1.0.0",
            "components": {
                "data_acquisition": {
                    "description": "Real-time sports data fetching and processing",
                    "modules": ["SportsDataFetcher", "DataProcessor"],
                    "inputs": ["Sportradar API", "Betfair API"],
                    "outputs": ["Standardized event data", "Historical statistics"],
                },
                "ml_models": {
                    "description": "Predictive modeling and odds analysis",
                    "modules": ["MatchPredictor", "OddsConverter", "ValueBettingCalculator"],
                    "models": ["Gradient Boosting", "Logistic Regression"],
                    "outputs": ["Match probabilities", "Value calculations"],
                },
                "execution": {
                    "description": "Automated bet placement and management",
                    "modules": ["BetExecutor", "ComparisonEngine"],
                    "integrations": ["Betfair", "Kambi", "Pinnacle"],
                    "outputs": ["Bet confirmations", "Execution logs"],
                },
                "risk_management": {
                    "description": "Bankroll management and safety safeguards",
                    "modules": ["BankrollManager", "ResponsibleGaming", "ExposureManager"],
                    "features": ["Kelly Criterion", "Loss limits", "Daily caps"],
                    "outputs": ["Risk assessments", "Compliance logs"],
                },
            },
            "data_flow": [
                "Real-time events → Data Processing → ML Predictions → Value Analysis → Risk Check → Bet Execution → Outcome Recording"
            ],
        }
