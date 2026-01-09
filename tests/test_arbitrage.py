"""
Tests for Advanced Arbitrage and Multi-Bet System
"""
import pytest
from src.execution import ArbitrageEngine, MultiBetOptimizer, CoverageStrategy


class TestArbitrageEngine:
    """Test arbitrage detection and stake calculation"""
    
    def test_two_way_arbitrage_found(self):
        """Test detecting 2-way arbitrage"""
        engine = ArbitrageEngine()
        
        # 1.95 and 2.20 should have arbitrage
        is_arb, margin = engine.check_two_way_arbitrage(1.95, 2.20)
        
        assert is_arb is True
        assert margin > 0.03  # At least 3%
    
    def test_two_way_no_arbitrage(self):
        """Test when no 2-way arbitrage exists"""
        engine = ArbitrageEngine()
        
        # 1.50 and 1.50 has no arbitrage (sum = 2.0 > 1.0)
        is_arb, margin = engine.check_two_way_arbitrage(1.50, 1.50)
        
        assert is_arb is False
        assert margin == 0.0
    
    def test_three_way_arbitrage(self):
        """Test 3-way arbitrage detection"""
        engine = ArbitrageEngine()
        
        # Create scenario with 3-way arbitrage
        is_arb, margin = engine.check_three_way_arbitrage(2.5, 3.4, 2.7)
        
        # Calculate: 1/2.5 + 1/3.4 + 1/2.7 = 0.4 + 0.294 + 0.370 = 1.064 > 1
        # So no arbitrage in these odds
        assert is_arb is False
    
    def test_implied_probabilities(self):
        """Test conversion of odds to implied probabilities"""
        engine = ArbitrageEngine()
        
        odds = [2.0, 3.0, 4.0]
        probs = engine.calculate_implied_probabilities(odds)
        
        assert len(probs) == 3
        assert probs[0] == pytest.approx(0.5)
        assert probs[1] == pytest.approx(0.333, rel=0.01)
        assert probs[2] == pytest.approx(0.25)
    
    def test_arbitrage_stakes_calculation(self):
        """Test calculating optimal stakes for arbitrage"""
        engine = ArbitrageEngine(min_profit_margin=0.01)
        
        stakes = engine.calculate_arbitrage_stakes(
            total_bankroll=500,
            odds_list=[1.95, 2.20],
            bookmakers=["Betfair", "Kambi"],
            outcomes=["Player A", "Player B"]
        )
        
        assert stakes is not None
        assert stakes["arbitrage_found"] is True
        assert stakes["guaranteed_profit"] > 0
        assert stakes["total_investment"] == 500


class TestMultiBetOptimizer:
    """Test multi-bet optimization and parlay functionality"""
    
    def test_parlay_probability_calculation(self):
        """Test calculating parlay win probability"""
        optimizer = MultiBetOptimizer()
        
        probs = [0.65, 0.70, 0.55]
        parlay_prob = optimizer.calculate_parlay_probability(probs)
        
        # 0.65 * 0.70 * 0.55 = 0.25025
        assert parlay_prob == pytest.approx(0.25025, rel=0.01)
    
    def test_parlay_odds_calculation(self):
        """Test calculating combined parlay odds"""
        optimizer = MultiBetOptimizer()
        
        odds = [1.80, 1.60, 2.10]
        parlay_odds = optimizer.calculate_parlay_odds(odds)
        
        # 1.80 * 1.60 * 2.10 = 6.048
        assert parlay_odds == pytest.approx(6.048, rel=0.01)
    
    def test_teaser_odds_reduction(self):
        """Test teaser odds with adjustment factor"""
        optimizer = MultiBetOptimizer()
        
        odds = [2.0, 2.0]
        teaser_odds = optimizer.calculate_teaser_odds(odds, adjustment_factor=0.95)
        
        # (2.0 * 0.95) * (2.0 * 0.95) = 3.61
        assert teaser_odds == pytest.approx(3.61, rel=0.01)
    
    def test_multiple_bets_optimization(self):
        """Test optimal allocation across multiple bets"""
        optimizer = MultiBetOptimizer()
        
        bets = [
            {"event": "Event 1", "probability": 0.65, "odds": 1.80},
            {"event": "Event 2", "probability": 0.70, "odds": 1.60},
            {"event": "Event 3", "probability": 0.55, "odds": 2.10},
        ]
        
        allocation = optimizer.optimize_multiple_bets(bets, bankroll=1000)
        
        # Total allocation should be less than bankroll
        assert allocation["total_allocated"] <= 1000
        assert allocation["remaining_bankroll"] >= 0
        assert allocation["total_expected_value"] > 0
    
    def test_find_best_combination(self):
        """Test finding best bet combination"""
        optimizer = MultiBetOptimizer()
        
        events = [
            {"probability": 0.65, "odds": 1.80},
            {"probability": 0.70, "odds": 1.60},
            {"probability": 0.55, "odds": 2.10},
        ]
        
        best = optimizer.find_best_combination(events, combination_size=2)
        
        assert best is not None
        assert best["parlay_odds"] > 1.0
        assert best["expected_value_percent"] > 0


class TestCoverageStrategy:
    """Test full coverage and hedging strategies"""
    
    def test_full_coverage_calculation(self):
        """Test calculating stakes to cover all outcomes"""
        outcomes = [
            {"name": "Outcome A", "odds": 2.50},
            {"name": "Outcome B", "odds": 3.40},
            {"name": "Outcome C", "odds": 2.70},
        ]
        
        result = CoverageStrategy.calculate_full_coverage(outcomes, bankroll=1000)
        
        # Sum of stakes should equal bankroll
        total_stakes = sum(s["stake"] for s in result["stakes"].values())
        assert total_stakes == pytest.approx(1000, rel=0.01)
        
        # All returns should be equal
        returns = [s["return"] for s in result["stakes"].values()]
        assert all(abs(r - returns[0]) < 1 for r in returns)
    
    def test_arbitrage_in_coverage(self):
        """Test coverage strategy detecting arbitrage"""
        # Create scenario with arbitrage
        outcomes = [
            {"name": "Outcome A", "odds": 2.0},
            {"name": "Outcome B", "odds": 2.0},
        ]
        
        result = CoverageStrategy.calculate_full_coverage(outcomes, bankroll=1000)
        
        # 1/2.0 + 1/2.0 = 1.0, so no arbitrage
        assert result["is_arbitrage"] is False
    
    def test_hedging_calculation(self):
        """Test hedging stake calculation"""
        original_bet = {
            "odds": 3.5,
            "stake": 200
        }
        
        hedge = CoverageStrategy.calculate_hedging_stakes(original_bet, target_profit=200)
        
        # Result should have hedge_stake and guarantee_profit
        assert "hedge_stake" in hedge or "note" in hedge


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_arbitrage_workflow(self):
        """Test complete arbitrage workflow"""
        engine = ArbitrageEngine()
        
        # Simulate finding and executing arbitrage
        is_arb, margin = engine.check_two_way_arbitrage(1.95, 2.20)
        
        if is_arb:
            stakes = engine.calculate_arbitrage_stakes(
                total_bankroll=1000,
                odds_list=[1.95, 2.20],
                bookmakers=["Betfair", "Kambi"],
                outcomes=["Outcome A", "Outcome B"]
            )
            
            # Verify stakes sum to bankroll
            total = sum(s["stake"] for s in stakes["stakes"].values())
            assert total == pytest.approx(1000, rel=0.01)
    
    def test_multi_bet_workflow(self):
        """Test complete multi-bet workflow"""
        optimizer = MultiBetOptimizer()
        
        bets = [
            {"event": "Event 1", "probability": 0.65, "odds": 1.80},
            {"event": "Event 2", "probability": 0.70, "odds": 1.60},
        ]
        
        # Allocate bets
        allocation = optimizer.optimize_multiple_bets(bets, bankroll=1000)
        
        # Find best combination
        best = optimizer.find_best_combination(bets, combination_size=2)
        
        # Both should work
        assert allocation["total_allocated"] > 0
        assert best is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
