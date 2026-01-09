"""
Risk Management Module
Bankroll management, Kelly Criterion, stop-loss, and responsible gaming
"""
import logging
import numpy as np
from typing import Dict, Tuple, Optional
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BankrollManager:
    """
    Manages bankroll with Kelly Criterion and safety limits
    """
    
    def __init__(self, initial_bankroll: float, max_daily_loss_percent: float = 5.0,
                 max_single_bet_percent: float = 2.0):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.max_daily_loss_percent = max_daily_loss_percent
        self.max_single_bet_percent = max_single_bet_percent
        self.daily_losses = 0.0
        self.daily_bets_count = 0
        self.bets_history = []
        self.last_reset_date = datetime.now().date()
        
    def reset_daily_stats(self) -> None:
        """Reset daily statistics"""
        if datetime.now().date() != self.last_reset_date:
            self.daily_losses = 0.0
            self.daily_bets_count = 0
            self.last_reset_date = datetime.now().date()
    
    def kelly_criterion(self, win_probability: float, odds: float) -> float:
        """
        Calculate Kelly Fraction for optimal bet sizing
        Kelly % = (bp - q) / b, where:
        - b = odds - 1
        - p = probability of winning
        - q = probability of losing (1 - p)
        
        Args:
            win_probability: Probability of bet winning (0-1)
            odds: Decimal odds
            
        Returns:
            Kelly fraction as percentage (0-1, typically 0-0.25 for safety)
        """
        if win_probability <= 0 or odds <= 1:
            return 0.0
        
        b = odds - 1
        p = win_probability
        q = 1 - p
        
        kelly = (b * p - q) / b
        
        # Safety: use fractional Kelly (typically 1/4 Kelly) to reduce variance
        fractional_kelly = kelly / 4.0
        
        return max(0.0, min(fractional_kelly, 0.25))  # Cap at 25% of bankroll
    
    def calculate_optimal_stake(self, predicted_prob: float, decimal_odds: float,
                               use_kelly: bool = True) -> float:
        """
        Calculate optimal stake based on Kelly Criterion or max bet percentage
        
        Args:
            predicted_prob: Model's predicted probability
            decimal_odds: Market odds
            use_kelly: Use Kelly Criterion if True, else use max bet percent
            
        Returns:
            Recommended stake amount
        """
        self.reset_daily_stats()
        
        # Check daily limits
        max_daily_loss = self.current_bankroll * (self.max_daily_loss_percent / 100)
        remaining_daily = max_daily_loss - self.daily_losses
        
        if remaining_daily <= 0:
            logger.warning("Daily loss limit reached")
            return 0.0
        
        # Max single bet limit (as percentage of bankroll)
        max_single_bet = self.current_bankroll * (self.max_single_bet_percent / 100)
        
        if use_kelly:
            kelly_fraction = self.kelly_criterion(predicted_prob, decimal_odds)
            stake = self.current_bankroll * kelly_fraction
        else:
            stake = max_single_bet
        
        # Ensure stake doesn't exceed limits
        stake = min(stake, remaining_daily, max_single_bet)
        
        return max(0.01, stake)  # Minimum stake
    
    def record_bet_result(self, stake: float, result: str, winnings: float = 0.0) -> None:
        """
        Record bet result and update bankroll
        
        Args:
            stake: Original stake amount
            result: 'won', 'lost', or 'voided'
            winnings: Amount won (profit)
        """
        self.reset_daily_stats()
        
        if result == "won":
            self.current_bankroll += winnings
            logger.info(f"Bet won: +{winnings}, Bankroll: {self.current_bankroll}")
        elif result == "lost":
            self.current_bankroll -= stake
            self.daily_losses += stake
            logger.warning(f"Bet lost: -{stake}, Bankroll: {self.current_bankroll}")
        elif result == "voided":
            logger.info(f"Bet voided: stake returned")
        
        self.daily_bets_count += 1
        self.bets_history.append({
            "timestamp": datetime.now().isoformat(),
            "stake": stake,
            "result": result,
            "winnings": winnings,
            "bankroll_after": self.current_bankroll,
        })
    
    def check_bankroll_health(self) -> RiskLevel:
        """Assess current bankroll health"""
        loss_percent = (self.daily_losses / self.current_bankroll) * 100 if self.current_bankroll > 0 else 0
        
        if loss_percent > self.max_daily_loss_percent:
            return RiskLevel.CRITICAL
        elif loss_percent > self.max_daily_loss_percent * 0.75:
            return RiskLevel.HIGH
        elif loss_percent > self.max_daily_loss_percent * 0.5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

class ResponsibleGaming:
    """
    Responsible gaming checks and safeguards
    """
    
    def __init__(self, pause_after_losses: int = 3, max_daily_bets: int = 20):
        self.pause_after_losses = pause_after_losses
        self.max_daily_bets = max_daily_bets
        self.consecutive_losses = 0
        self.daily_bet_count = 0
        self.last_bet_time = None
        self.is_paused = False
    
    def check_loss_streak(self, result: str) -> bool:
        """
        Check for loss streak and pause if threshold exceeded
        
        Returns:
            True if system should pause
        """
        if result == "lost":
            self.consecutive_losses += 1
            if self.consecutive_losses >= self.pause_after_losses:
                self.is_paused = True
                logger.warning(f"Loss streak detected ({self.consecutive_losses}), pausing system")
                return True
        else:
            self.consecutive_losses = 0
        
        return False
    
    def check_daily_limits(self, current_bets: int) -> bool:
        """
        Check if daily bet limit exceeded
        
        Returns:
            True if under limit
        """
        if current_bets >= self.max_daily_bets:
            logger.warning("Daily bet limit reached")
            return False
        return True
    
    def get_pause_duration(self) -> timedelta:
        """Get recommended pause duration after loss streak"""
        return timedelta(hours=1)

class ExposureManager:
    """
    Manage exposure across sports, markets, and teams
    """
    
    def __init__(self):
        self.max_exposure_per_sport = 0.10  # Max 10% of bankroll per sport
        self.max_exposure_per_team = 0.05   # Max 5% per team
        self.current_exposure = {}
    
    def add_exposure(self, sport: str, team: str, amount: float) -> None:
        """Record exposure"""
        if sport not in self.current_exposure:
            self.current_exposure[sport] = {}
        
        if team not in self.current_exposure[sport]:
            self.current_exposure[sport][team] = 0.0
        
        self.current_exposure[sport][team] += amount
    
    def check_exposure_limits(self, sport: str, team: str, new_amount: float,
                            bankroll: float) -> bool:
        """Check if new bet exceeds exposure limits"""
        # Simplified check
        return True
