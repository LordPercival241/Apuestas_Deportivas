"""
Unit Tests for Sports Betting System
"""
import pytest
import numpy as np
from src.ml_models import MatchPredictor, ValueBettingCalculator, OddsConverter
from src.risk_management import BankrollManager, ResponsibleGaming
from src.execution import BetExecutor
from src.data_acquisition import SportsDataFetcher

class TestMatchPredictor:
    def test_kelly_criterion(self):
        bankroll = BankrollManager(1000)
        kelly = bankroll.kelly_criterion(0.65, 1.80)
        assert 0 <= kelly <= 0.25
        assert kelly > 0  # Positive edge
    
    def test_kelly_criterion_no_edge(self):
        bankroll = BankrollManager(1000)
        kelly = bankroll.kelly_criterion(0.50, 1.80)
        assert kelly >= 0  # Should be zero or positive
    
    def test_optimal_stake_calculation(self):
        bankroll = BankrollManager(1000)
        stake = bankroll.calculate_optimal_stake(0.65, 1.80)
        assert 0 < stake <= 1000
        assert stake <= 1000 * 0.02  # Max single bet percent

class TestValueBetting:
    def test_value_calculation_positive(self):
        value = ValueBettingCalculator.calculate_value(0.65, 1.80)
        assert value > 0
        assert value == pytest.approx(0.17, rel=0.01)
    
    def test_value_calculation_zero(self):
        value = ValueBettingCalculator.calculate_value(0.50, 2.0)
        assert value == pytest.approx(0.0, abs=0.01)
    
    def test_has_value_threshold(self):
        assert ValueBettingCalculator.has_value(0.65, 1.80, 0.05)
        assert not ValueBettingCalculator.has_value(0.55, 1.80, 0.10)

class TestOddsConversion:
    def test_decimal_to_probability(self):
        prob = OddsConverter.decimal_to_probability(2.0)
        assert prob == pytest.approx(0.50)
        
        prob = OddsConverter.decimal_to_probability(1.80)
        assert prob == pytest.approx(0.556, rel=0.01)
    
    def test_probability_to_decimal(self):
        odds = OddsConverter.probability_to_decimal(0.50)
        assert odds == pytest.approx(2.0)

class TestBankrollManager:
    def test_initial_bankroll(self):
        bm = BankrollManager(1000.0)
        assert bm.current_bankroll == 1000.0
    
    def test_record_win(self):
        bm = BankrollManager(1000.0)
        bm.record_bet_result(100.0, "won", 80.0)
        assert bm.current_bankroll == 1080.0
    
    def test_record_loss(self):
        bm = BankrollManager(1000.0)
        bm.record_bet_result(100.0, "lost")
        assert bm.current_bankroll == 900.0
        assert bm.daily_losses == 100.0

class TestResponsibleGaming:
    def test_loss_streak_detection(self):
        rg = ResponsibleGaming(pause_after_losses=3)
        
        assert not rg.check_loss_streak("lost")  # 1st loss
        assert not rg.check_loss_streak("lost")  # 2nd loss
        assert rg.check_loss_streak("lost")      # 3rd loss - should pause
        assert rg.is_paused
    
    def test_loss_streak_reset(self):
        rg = ResponsibleGaming(pause_after_losses=3)
        
        rg.check_loss_streak("lost")
        rg.check_loss_streak("lost")
        result = rg.check_loss_streak("won")  # Win resets counter
        assert not result  # Should not pause on win
        assert rg.consecutive_losses == 0  # Counter should be reset

class TestBetExecutor:
    def test_bet_validation(self):
        executor = BetExecutor()
        
        # Valid bet
        valid_bet = {
            "event_id": "evt_123",
            "market_id": "market_123",
            "odds": 1.80,
            "stake": 25.0,
            "bet_type": "back",
            "selection": "home_win",
        }
        assert executor.validate_bet(valid_bet)
        
        # Invalid odds
        invalid_bet = valid_bet.copy()
        invalid_bet["odds"] = 0.50
        assert not executor.validate_bet(invalid_bet)
        
        # Invalid stake
        invalid_bet = valid_bet.copy()
        invalid_bet["stake"] = 0.001
        assert not executor.validate_bet(invalid_bet)

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
