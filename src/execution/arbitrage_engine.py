"""
Advanced Arbitrage Engine
Multi-way arbitrage and guaranteed profit detection
"""
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from itertools import combinations

logger = logging.getLogger(__name__)


class ArbitrageEngine:
    """
    Detect and calculate arbitrage opportunities across multiple bookmakers
    and multiple outcomes with guaranteed profit potential
    """

    def __init__(self, min_profit_margin: float = 0.01):
        """
        Args:
            min_profit_margin: Minimum profit percentage to consider arbitrage (default 1%)
        """
        self.min_profit_margin = min_profit_margin
        self.arbitrage_opportunities = []

    @staticmethod
    def calculate_implied_probabilities(odds_list: List[float]) -> List[float]:
        """
        Convert decimal odds to implied probabilities
        
        Args:
            odds_list: List of decimal odds
            
        Returns:
            List of implied probabilities
        """
        return [1.0 / odds for odds in odds_list if odds > 0]

    @staticmethod
    def check_two_way_arbitrage(odds_1: float, odds_2: float) -> Tuple[bool, float]:
        """
        Check for 2-way arbitrage (binary outcome)
        
        Args:
            odds_1: Odds for outcome 1
            odds_2: Odds for outcome 2
            
        Returns:
            (is_arbitrage, profit_margin)
        """
        if odds_1 <= 1 or odds_2 <= 1:
            return False, 0.0

        inv_odds_sum = (1.0 / odds_1) + (1.0 / odds_2)
        
        if inv_odds_sum < 1.0:
            profit_margin = (1.0 - inv_odds_sum) / inv_odds_sum
            return True, profit_margin
        
        return False, 0.0

    @staticmethod
    def check_three_way_arbitrage(odds_1: float, odds_2: float, odds_3: float) -> Tuple[bool, float]:
        """
        Check for 3-way arbitrage (3 possible outcomes: home win, draw, away win)
        
        Args:
            odds_1: Odds for outcome 1 (home win)
            odds_2: Odds for outcome 2 (draw)
            odds_3: Odds for outcome 3 (away win)
            
        Returns:
            (is_arbitrage, profit_margin)
        """
        if odds_1 <= 1 or odds_2 <= 1 or odds_3 <= 1:
            return False, 0.0

        inv_odds_sum = (1.0 / odds_1) + (1.0 / odds_2) + (1.0 / odds_3)
        
        if inv_odds_sum < 1.0:
            profit_margin = (1.0 - inv_odds_sum) / inv_odds_sum
            return True, profit_margin
        
        return False, 0.0

    def calculate_arbitrage_stakes(self, total_bankroll: float, odds_list: List[float],
                                  bookmakers: List[str], outcomes: List[str]) -> Optional[Dict]:
        """
        Calculate optimal stakes for each outcome to guarantee profit
        
        Args:
            total_bankroll: Total amount to invest
            odds_list: List of odds for each outcome
            bookmakers: List of bookmaker names
            outcomes: List of outcome descriptions
            
        Returns:
            Dictionary with stake allocation or None if no arbitrage
        """
        num_outcomes = len(odds_list)
        
        if num_outcomes < 2:
            return None

        # Calculate implied probabilities (total stake proportions)
        inv_odds = [1.0 / odds for odds in odds_list]
        inv_odds_sum = sum(inv_odds)
        
        # Check if arbitrage exists
        if inv_odds_sum >= 1.0:
            return None
        
        # Calculate profit margin
        profit_margin = (1.0 - inv_odds_sum) / inv_odds_sum
        
        if profit_margin < self.min_profit_margin:
            return None
        
        # Calculate stakes for each outcome
        stakes = {}
        for i, outcome in enumerate(outcomes):
            stake = (total_bankroll * inv_odds[i]) / inv_odds_sum
            stakes[outcome] = {
                "stake": stake,
                "odds": odds_list[i],
                "bookmaker": bookmakers[i],
                "guaranteed_return": stake * odds_list[i],
            }
        
        return {
            "arbitrage_found": True,
            "total_investment": total_bankroll,
            "guaranteed_profit": total_bankroll * profit_margin,
            "profit_margin_percent": profit_margin * 100,
            "roi_percent": (profit_margin / 1.0) * 100,
            "stakes": stakes,
            "num_outcomes": num_outcomes,
        }

    def find_market_arbitrage(self, market_data: Dict) -> Optional[Dict]:
        """
        Find arbitrage in a complete market (all outcomes covered)
        
        Args:
            market_data: Dictionary with outcomes and their best odds across bookmakers
                {
                    "home_win": {"betfair": 2.50, "kambi": 2.48, ...},
                    "draw": {"betfair": 3.20, "pinnacle": 3.10, ...},
                    "away_win": {"betfair": 3.10, "kambi": 3.15, ...}
                }
                
        Returns:
            Arbitrage opportunity or None
        """
        outcomes = list(market_data.keys())
        
        if len(outcomes) < 2:
            return None
        
        # Get best odds for each outcome
        best_odds = []
        best_bookmakers = []
        
        for outcome in outcomes:
            bookmaker_odds = market_data[outcome]
            best_odd = max(bookmaker_odds.values())
            best_bookie = max(bookmaker_odds, key=bookmaker_odds.get)
            
            best_odds.append(best_odd)
            best_bookmakers.append(best_bookie)
        
        # Check for arbitrage
        if len(best_odds) == 2:
            is_arb, margin = self.check_two_way_arbitrage(best_odds[0], best_odds[1])
        elif len(best_odds) == 3:
            is_arb, margin = self.check_three_way_arbitrage(*best_odds)
        else:
            # N-way arbitrage
            inv_odds_sum = sum(1.0 / odds for odds in best_odds)
            is_arb = inv_odds_sum < 1.0
            margin = (1.0 - inv_odds_sum) / inv_odds_sum if is_arb else 0.0
        
        if not is_arb or margin < self.min_profit_margin:
            return None
        
        return {
            "arbitrage_found": True,
            "outcomes": outcomes,
            "best_odds": best_odds,
            "bookmakers": best_bookmakers,
            "profit_margin": margin,
            "profit_margin_percent": margin * 100,
        }


class MultiBetOptimizer:
    """
    Optimize multiple bets for maximum expected value
    Handles correlated outcomes and combination strategies
    """

    def __init__(self):
        self.kelly_fraction = 0.25  # Fractional Kelly for safety

    def calculate_parlay_probability(self, individual_probabilities: List[float]) -> float:
        """
        Calculate probability of winning a parlay (all bets must win)
        
        Args:
            individual_probabilities: List of win probabilities (0-1)
            
        Returns:
            Parlay win probability
        """
        if not individual_probabilities:
            return 0.0
        
        return np.prod(individual_probabilities)

    def calculate_parlay_odds(self, odds_list: List[float]) -> float:
        """
        Calculate combined odds for a parlay (multiply all odds)
        
        Args:
            odds_list: List of decimal odds
            
        Returns:
            Combined parlay odds
        """
        if not odds_list:
            return 1.0
        
        return np.prod(odds_list)

    def calculate_teaser_odds(self, odds_list: List[float], 
                            adjustment_factor: float = 0.95) -> float:
        """
        Calculate teaser odds (slightly worse odds but higher probability)
        
        Args:
            odds_list: List of decimal odds
            adjustment_factor: Factor to adjust each odd (< 1.0 means worse odds)
            
        Returns:
            Adjusted teaser odds
        """
        adjusted_odds = [odds * adjustment_factor for odds in odds_list]
        return np.prod(adjusted_odds)

    def optimize_multiple_bets(self, bets: List[Dict], bankroll: float) -> Dict:
        """
        Optimize allocation across multiple independent bets
        
        Args:
            bets: List of bet dictionaries
                {
                    "event": "event_name",
                    "probability": 0.65,
                    "odds": 1.80,
                    "bookmaker": "betfair"
                }
            bankroll: Total bankroll to allocate
            
        Returns:
            Optimized bet allocation
        """
        allocations = {}
        total_allocation = 0.0
        
        for i, bet in enumerate(bets):
            prob = bet.get("probability", 0.5)
            odds = bet.get("odds", 1.5)
            
            # Kelly Criterion for this bet
            if odds > 1:
                b = odds - 1
                p = prob
                q = 1 - p
                kelly = (b * p - q) / b if b > 0 else 0
            else:
                kelly = 0
            
            # Fractional Kelly for safety
            kelly_fraction = kelly * self.kelly_fraction
            
            # Allocation
            stake = bankroll * max(0, kelly_fraction)
            
            allocations[f"bet_{i}"] = {
                "event": bet.get("event"),
                "stake": stake,
                "probability": prob,
                "odds": odds,
                "kelly_percent": kelly_fraction * 100,
                "expected_value": stake * (prob * odds - 1),
            }
            
            total_allocation += stake
        
        return {
            "total_allocated": total_allocation,
            "remaining_bankroll": bankroll - total_allocation,
            "allocations": allocations,
            "total_expected_value": sum(v["expected_value"] for v in allocations.values()),
        }

    def find_best_combination(self, events: List[Dict], 
                            combination_size: int = 2) -> Optional[Dict]:
        """
        Find the best combination of bets for a parlay/teaser
        
        Args:
            events: List of event dictionaries with probability and odds
            combination_size: Number of events to combine
            
        Returns:
            Best combination for maximum expected value
        """
        if len(events) < combination_size:
            return None
        
        best_combination = None
        best_ev = 0.0
        
        # Generate all combinations
        for combo in combinations(range(len(events)), combination_size):
            selected_events = [events[i] for i in combo]
            
            # Calculate parlay probability and odds
            probs = [e.get("probability", 0.5) for e in selected_events]
            odds_list = [e.get("odds", 1.5) for e in selected_events]
            
            parlay_prob = self.calculate_parlay_probability(probs)
            parlay_odds = self.calculate_parlay_odds(odds_list)
            
            # Expected value per unit stake
            ev = parlay_prob * parlay_odds - 1.0
            
            if ev > best_ev:
                best_ev = ev
                best_combination = {
                    "events": selected_events,
                    "event_indices": combo,
                    "parlay_probability": parlay_prob,
                    "parlay_odds": parlay_odds,
                    "expected_value_percent": ev * 100,
                    "stake_recommendation": "1 unit per $100 bankroll" if ev > 0.05 else "Skip - Low EV",
                }
        
        return best_combination if best_ev > 0 else None


class CoverageStrategy:
    """
    Create betting strategies that cover all outcomes
    Guarantees profit or loss control
    """

    @staticmethod
    def calculate_full_coverage(outcomes: List[Dict], bankroll: float) -> Dict:
        """
        Calculate stakes to cover all outcomes and guarantee return
        
        Args:
            outcomes: List with format [{"name": "outcome1", "odds": 2.5}, ...]
            bankroll: Total amount to invest
            
        Returns:
            Stake distribution to cover all outcomes
        """
        if not outcomes:
            return {}
        
        # Calculate inverse odds (probability implied)
        inv_odds = [1.0 / o["odds"] for o in outcomes]
        inv_odds_sum = sum(inv_odds)
        
        # If sum > 1, there's no arbitrage but we can cover
        # If sum < 1, there's guaranteed profit
        
        stakes = {}
        for i, outcome in enumerate(outcomes):
            # Stake proportional to inverse odds
            stake = (bankroll * inv_odds[i]) / inv_odds_sum
            stakes[outcome["name"]] = {
                "stake": stake,
                "odds": outcome["odds"],
                "return": stake * outcome["odds"],
            }
        
        return {
            "is_arbitrage": inv_odds_sum < 1.0,
            "profit_margin": (1.0 - inv_odds_sum) / inv_odds_sum if inv_odds_sum > 0 else 0,
            "stakes": stakes,
            "guaranteed_return": bankroll if inv_odds_sum >= 1.0 else bankroll / inv_odds_sum,
        }

    @staticmethod
    def calculate_hedging_stakes(original_bet: Dict, target_profit: float) -> Dict:
        """
        Calculate hedging stakes to lock in profit or limit losses
        
        Args:
            original_bet: Original bet details {"odds": 2.5, "stake": 100, "current_value": 50}
            target_profit: Target profit amount
            
        Returns:
            Hedging stake to place
        """
        odds = original_bet.get("odds", 1.0)
        stake = original_bet.get("stake", 0.0)
        
        if odds <= 1:
            return {}
        
        # Hedge bet on opposite outcome
        # If original wins: profit = stake * (odds - 1) - hedge_stake
        # If original loses: profit = hedge_stake - stake - hedge_stake * hedge_odds
        
        return {
            "hedge_stake": target_profit / (1 - odds),
            "guarantees_profit": target_profit,
            "note": "Place hedge bet on opposite outcome"
        }
