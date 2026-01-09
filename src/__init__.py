"""
Sports Betting Autonomous System
Real-time monitoring, ML predictions, automated execution with risk management
"""

__version__ = "1.0.0"
__author__ = "Betting System Team"

# Import core modules
from src.data_acquisition import SportsDataFetcher, DataProcessor
from src.ml_models import MatchPredictor, OddsConverter, ValueBettingCalculator
from src.execution import BetExecutor, ComparisonEngine
from src.risk_management import BankrollManager, ResponsibleGaming, ExposureManager
from src.utils import setup_logging, AuditLogger

__all__ = [
    "SportsDataFetcher",
    "DataProcessor",
    "MatchPredictor",
    "OddsConverter",
    "ValueBettingCalculator",
    "BetExecutor",
    "ComparisonEngine",
    "BankrollManager",
    "ResponsibleGaming",
    "ExposureManager",
    "setup_logging",
    "AuditLogger",
]
