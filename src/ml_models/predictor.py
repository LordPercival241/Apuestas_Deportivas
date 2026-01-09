"""
ML Models Module
Predictive models for match outcomes and betting predictions
"""
import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from typing import Dict, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class MatchPredictor:
    """
    Machine Learning predictor for match outcomes
    Supports multiple models: Logistic Regression, XGBoost, etc.
    """
    
    def __init__(self, model_type: str = "gradient_boosting"):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
        if model_type == "gradient_boosting":
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif model_type == "logistic_regression":
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=42
            )
    
    def extract_features(self, match_data: Dict) -> np.ndarray:
        """
        Extract relevant features from match data
        
        Features include:
        - Team form (last 5 matches average)
        - Head-to-head record
        - Home advantage
        - Player availability (injuries)
        - Weather conditions
        - Season stage
        """
        features = {
            "home_team_form": match_data.get("home_form", 0.5),
            "away_team_form": match_data.get("away_form", 0.5),
            "home_advantage": 1.0,  # Home team advantage factor
            "head_to_head_home": match_data.get("h2h_home_wins", 0.5),
            "recent_goals_home": match_data.get("recent_goals_home", 1.5),
            "recent_goals_away": match_data.get("recent_goals_away", 1.0),
            "injuries_home": match_data.get("injuries_home_count", 0),
            "injuries_away": match_data.get("injuries_away_count", 0),
            "home_possession_avg": match_data.get("home_possession_avg", 50),
            "away_possession_avg": match_data.get("away_possession_avg", 50),
            "home_shots_on_target_avg": match_data.get("home_shots_avg", 4),
            "away_shots_on_target_avg": match_data.get("away_shots_avg", 3),
            "momentum_factor": match_data.get("momentum", 0.5),
        }
        
        self.feature_names = list(features.keys())
        return np.array(list(features.values())).reshape(1, -1)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the predictive model
        
        Args:
            X_train: Feature matrix
            y_train: Target labels (0: away win, 1: home win, 2: draw)
        """
        try:
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled, y_train)
            self.is_trained = True
            logger.info(f"Model trained successfully: {self.model_type}")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
    
    def predict_probability(self, match_data: Dict) -> Dict[str, float]:
        """
        Predict match outcome probabilities
        
        Returns:
            Dictionary with probabilities for each outcome
        """
        if not self.is_trained:
            logger.warning("Model not trained yet")
            return {}
        
        try:
            X = self.extract_features(match_data)
            X_scaled = self.scaler.transform(X)
            
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(X_scaled)[0]
            else:
                probabilities = self.model.predict(X_scaled)
            
            return {
                "home_win": float(probabilities[1] if len(probabilities) > 1 else probabilities[0]),
                "draw": float(probabilities[2] if len(probabilities) > 2 else 0.0),
                "away_win": float(probabilities[0] if len(probabilities) > 0 else 1 - probabilities[1]),
                "confidence": float(np.max(probabilities)),
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return {}
    
    def save_model(self, filepath: str) -> None:
        """Save trained model to disk"""
        try:
            joblib.dump({
                "model": self.model,
                "scaler": self.scaler,
                "feature_names": self.feature_names,
                "model_type": self.model_type,
            }, filepath)
            logger.info(f"Model saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self, filepath: str) -> None:
        """Load trained model from disk"""
        try:
            data = joblib.load(filepath)
            self.model = data["model"]
            self.scaler = data["scaler"]
            self.feature_names = data["feature_names"]
            self.model_type = data["model_type"]
            self.is_trained = True
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")

class OddsConverter:
    """
    Convert between different odds formats and calculate implied probabilities
    """
    
    @staticmethod
    def decimal_to_probability(odds: float) -> float:
        """Convert decimal odds to implied probability"""
        if odds > 0:
            return 1.0 / odds
        return 0.0
    
    @staticmethod
    def probability_to_decimal(probability: float) -> float:
        """Convert probability to decimal odds"""
        if probability > 0:
            return 1.0 / probability
        return 0.0
    
    @staticmethod
    def fractional_to_decimal(numerator: float, denominator: float) -> float:
        """Convert fractional odds to decimal (e.g., 5/1 -> 6.0)"""
        return (numerator / denominator) + 1.0
    
    @staticmethod
    def american_to_decimal(american_odds: float) -> float:
        """Convert American odds to decimal"""
        if american_odds > 0:
            return (american_odds / 100) + 1.0
        else:
            return (100 / abs(american_odds)) + 1.0

class ValueBettingCalculator:
    """
    Calculate value bets based on model predictions vs market odds
    Value = (predicted_probability × decimal_odds) - 1
    """
    
    @staticmethod
    def calculate_value(predicted_prob: float, decimal_odds: float) -> float:
        """
        Calculate betting value
        Positive value = Expected profit opportunity
        """
        return (predicted_prob * decimal_odds) - 1.0
    
    @staticmethod
    def has_value(predicted_prob: float, decimal_odds: float, min_threshold: float = 0.05) -> bool:
        """Check if bet has positive value above threshold"""
        value = ValueBettingCalculator.calculate_value(predicted_prob, decimal_odds)
        return value > min_threshold
    
    @staticmethod
    def expected_value_units(stake: float, value: float) -> float:
        """Calculate expected value in units"""
        return stake * value
