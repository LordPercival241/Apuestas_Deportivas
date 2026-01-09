"""
Zero-Investment System
Generate capital from bonuses, promotions, and simulated trading
"""
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class BonusType(Enum):
    """Types of available bonuses"""
    WELCOME_BONUS = "welcome_bonus"
    DEPOSIT_MATCH = "deposit_match"
    RISK_FREE_BET = "risk_free_bet"
    FREE_BET = "free_bet"
    CASHBACK = "cashback"
    REFERRAL = "referral"
    SEASONAL = "seasonal"


class BonusManager:
    """
    Manage bookmaker bonuses and promotional offers
    Extract maximum value from free money and promotions
    """

    def __init__(self):
        self.available_bonuses = {}
        self.used_bonuses = []
        self.total_bonus_value = 0.0

    def add_bonus(self, bookmaker: str, bonus: Dict) -> None:
        """
        Add an available bonus
        
        Args:
            bookmaker: Name of bookmaker
            bonus: {
                "type": BonusType,
                "amount": 50.0,
                "min_odds": 1.5,
                "rollover": 5,  # How many times to bet the bonus
                "expiry_days": 30,
                "description": "100% match up to $50"
            }
        """
        if bookmaker not in self.available_bonuses:
            self.available_bonuses[bookmaker] = []

        self.available_bonuses[bookmaker].append({
            **bonus,
            "added_date": datetime.now().isoformat(),
            "used": False,
        })

        self.total_bonus_value += bonus.get("amount", 0)

    def get_best_bonuses(self, min_amount: float = 0) -> List[Dict]:
        """
        Get bonuses ranked by value (amount / rollover requirement)
        
        Returns:
            Sorted list of bonuses
        """
        all_bonuses = []

        for bookmaker, bonuses in self.available_bonuses.items():
            for bonus in bonuses:
                if not bonus["used"] and bonus.get("amount", 0) >= min_amount:
                    # Efficiency score: amount / rollover
                    efficiency = bonus.get("amount", 0) / max(1, bonus.get("rollover", 5))
                    all_bonuses.append({
                        **bonus,
                        "bookmaker": bookmaker,
                        "efficiency_score": efficiency,
                    })

        # Sort by efficiency (best value first)
        return sorted(all_bonuses, key=lambda x: x["efficiency_score"], reverse=True)

    def calculate_bonus_strategy(self, bankroll: float = 0) -> Dict:
        """
        Calculate strategy to maximize bonus extraction
        
        Args:
            bankroll: Your own capital (can be 0)
            
        Returns:
            Strategy for using bonuses optimally
        """
        best_bonuses = self.get_best_bonuses()

        if not best_bonuses:
            return {"strategy": "No bonuses available", "total_potential": 0}

        strategy = {
            "total_bonuses_available": len(best_bonuses),
            "total_bonus_value": sum(b.get("amount", 0) for b in best_bonuses),
            "bonuses_by_priority": [],
            "recommended_sequence": [],
            "total_potential_earnings": 0,
        }

        # Sequence bonuses by efficiency
        for i, bonus in enumerate(best_bonuses[:5], 1):  # Top 5 bonuses
            rollover = bonus.get("rollover", 5)
            amount = bonus.get("amount", 0)
            min_odds = bonus.get("min_odds", 1.5)

            # Calculate how much profit is realistically achievable
            # Conservative estimate: 50% of bonus through low-risk bets
            potential_profit = amount * 0.5

            strategy["bonuses_by_priority"].append({
                "rank": i,
                "bookmaker": bonus.get("bookmaker"),
                "amount": amount,
                "rollover_requirement": rollover,
                "min_odds": min_odds,
                "efficiency_score": bonus.get("efficiency_score"),
                "potential_profit": potential_profit,
                "steps": [
                    f"1. Get ${amount} bonus",
                    f"2. Place {rollover}x rollover bets at {min_odds}+ odds",
                    f"3. Extract ~${potential_profit} profit",
                    f"4. Withdraw or reinvest",
                ]
            })

            strategy["total_potential_earnings"] += potential_profit

        return strategy

    def mark_bonus_used(self, bookmaker: str, bonus_index: int = 0) -> None:
        """Mark a bonus as used"""
        if bookmaker in self.available_bonuses:
            if bonus_index < len(self.available_bonuses[bookmaker]):
                self.available_bonuses[bookmaker][bonus_index]["used"] = True


class PaperTradingSimulator:
    """
    Simulate betting with virtual money
    Practice strategies without real money risk
    """

    def __init__(self, virtual_bankroll: float = 100.0):
        self.virtual_bankroll = virtual_bankroll
        self.initial_bankroll = virtual_bankroll
        self.virtual_bets = []
        self.daily_stats = {}

    def place_virtual_bet(self, event: str, odds: float, stake: float,
                         predicted_outcome: bool = True) -> Dict:
        """
        Place a simulated bet
        
        Args:
            event: Event description
            odds: Decimal odds
            stake: Bet amount
            predicted_outcome: Whether prediction was correct
            
        Returns:
            Bet result
        """
        if stake > self.virtual_bankroll:
            return {
                "success": False,
                "reason": f"Insufficient balance. Have ${self.virtual_bankroll:.2f}, need ${stake:.2f}"
            }

        # Simulate bet
        if predicted_outcome:
            winnings = stake * (odds - 1)
            self.virtual_bankroll += winnings
            result = "WON"
        else:
            self.virtual_bankroll -= stake
            winnings = -stake
            result = "LOST"

        bet_record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "odds": odds,
            "stake": stake,
            "result": result,
            "winnings": winnings,
            "bankroll_after": self.virtual_bankroll,
        }

        self.virtual_bets.append(bet_record)

        return {
            "success": True,
            "bet": bet_record,
            "bankroll_now": self.virtual_bankroll,
            "profit_so_far": self.virtual_bankroll - self.initial_bankroll,
        }

    def get_statistics(self) -> Dict:
        """Get performance statistics"""
        if not self.virtual_bets:
            return {"message": "No bets placed yet"}

        total_bets = len(self.virtual_bets)
        wins = sum(1 for b in self.virtual_bets if b["result"] == "WON")
        losses = total_bets - wins

        total_wagered = sum(b["stake"] for b in self.virtual_bets)
        total_profit = self.virtual_bankroll - self.initial_bankroll

        return {
            "total_bets": total_bets,
            "wins": wins,
            "losses": losses,
            "win_rate": wins / total_bets if total_bets > 0 else 0,
            "total_wagered": total_wagered,
            "current_bankroll": self.virtual_bankroll,
            "initial_bankroll": self.initial_bankroll,
            "total_profit": total_profit,
            "roi_percent": (total_profit / self.initial_bankroll * 100) if self.initial_bankroll > 0 else 0,
            "average_bet": total_wagered / total_bets if total_bets > 0 else 0,
        }


class FreeArbitrageStrategy:
    """
    Strategy to extract arbitrage using free bets and bonuses only
    Zero investment, only promotional money
    """

    @staticmethod
    def find_bonus_arbitrage(bonuses: List[Dict], odds_markets: List[Dict]) -> Optional[Dict]:
        """
        Find arbitrage that can be executed with bonus money only
        
        Args:
            bonuses: Available bonuses [{"bookmaker": "X", "amount": 50, "min_odds": 1.5}]
            odds_markets: Available odds markets for arbitrage
            
        Returns:
            Arbitrage strategy using only bonuses
        """
        if not bonuses:
            return None

        # Sort bonuses by amount (descending)
        bonuses = sorted(bonuses, key=lambda x: x.get("amount", 0), reverse=True)

        # For each bonus, find if it can be used in arbitrage
        for bonus in bonuses:
            bonus_amount = bonus.get("amount", 0)
            min_odds = bonus.get("min_odds", 1.5)

            # Find arbitrage with these constraints
            for market in odds_markets:
                odds_list = market.get("odds", [])

                # Check for arbitrage
                inv_odds_sum = sum(1.0 / odds for odds in odds_list if odds > 1)

                if inv_odds_sum < 1.0:
                    profit_margin = (1.0 - inv_odds_sum) / inv_odds_sum
                    all_odds_above_min = all(odds >= min_odds for odds in odds_list)

                    if all_odds_above_min:
                        return {
                            "found": True,
                            "bonus_bookmaker": bonus.get("bookmaker"),
                            "bonus_amount": bonus_amount,
                            "market": market.get("name"),
                            "odds": odds_list,
                            "profit_margin": profit_margin,
                            "profit_percent": profit_margin * 100,
                            "note": f"Use ${bonus_amount} bonus to execute arbitrage for ${bonus_amount * profit_margin:.2f} profit"
                        }

        return None

    @staticmethod
    def calculate_bonus_growth_path(starting_bonus: float = 50,
                                    win_rate: float = 0.55,
                                    bet_size_percent: float = 0.10) -> Dict:
        """
        Calculate realistic growth path from bonus money
        
        Args:
            starting_bonus: Initial bonus amount
            win_rate: Realistic win rate (0.55 = 55%)
            bet_size_percent: Percentage of bankroll to bet per bet
            
        Returns:
            Growth projection
        """
        bankroll = starting_bonus
        history = [{"day": 0, "bankroll": bankroll}]

        # Simulate 30 days of betting
        for day in range(1, 31):
            # 5 bets per day with average 2.0 odds
            daily_bets = 5
            daily_profit = 0

            for _ in range(daily_bets):
                stake = bankroll * bet_size_percent
                if stake < 1:
                    break

                # 55% win rate at 2.0 odds
                if win_rate > 0.5:  # Only if profitable expectation
                    expected_value = stake * (win_rate * 2.0 - 1)
                    daily_profit += expected_value

            bankroll += daily_profit
            history.append({"day": day, "bankroll": bankroll})

        return {
            "starting_bonus": starting_bonus,
            "projected_bankroll_day_30": bankroll,
            "total_growth": bankroll - starting_bonus,
            "growth_percent": ((bankroll - starting_bonus) / starting_bonus * 100) if starting_bonus > 0 else 0,
            "daily_history": history,
        }


class PromotionOptimizer:
    """
    Optimize use of all available promotions and bonuses
    """

    def __init__(self):
        self.available_promotions = []

    def add_promotion(self, promotion: Dict) -> None:
        """
        Add a promotion
        
        Args:
            promotion: {
                "bookmaker": "Betfair",
                "type": "welcome_bonus",
                "amount": 50,
                "min_deposit": 50,
                "rollover": 5,
                "expires_days": 30,
                "description": "Match your first deposit"
            }
        """
        self.available_promotions.append({
            **promotion,
            "added_date": datetime.now().isoformat(),
            "status": "available"
        })

    def calculate_free_capital_potential(self) -> Dict:
        """
        Calculate total free capital available from all promotions
        """
        total_free = 0
        total_required_deposit = 0
        promotion_list = []

        for promo in self.available_promotions:
            if promo["status"] == "available":
                bonus_amount = promo.get("amount", 0)
                min_deposit = promo.get("min_deposit", 0)

                # If min_deposit is required and you don't have it, it counts
                # But if it's a pure free bet with no deposit, it's 100% free
                if min_deposit == 0 or "free" in promo.get("type", "").lower():
                    free_portion = bonus_amount
                    deposit_required = 0
                else:
                    # Match promotions require you to deposit
                    # But the bonus itself is free
                    free_portion = bonus_amount
                    deposit_required = min_deposit

                total_free += free_portion
                total_required_deposit += deposit_required

                promotion_list.append({
                    "bookmaker": promo.get("bookmaker"),
                    "type": promo.get("type"),
                    "free_amount": free_portion,
                    "required_deposit": deposit_required,
                    "rollover": promo.get("rollover", 1),
                    "expires_days": promo.get("expires_days"),
                })

        return {
            "total_free_capital": total_free,
            "total_deposits_needed": total_required_deposit,
            "number_of_promotions": len(promotion_list),
            "promotions": promotion_list,
            "strategy": "Start with deposit-free bonuses, then use free bets from arbitrage to fund deposit matches" if total_free > 0 else "No free promotions available",
        }

    @staticmethod
    def recommended_sequence() -> List[Dict]:
        """
        Recommended sequence for maximizing free capital
        """
        return [
            {
                "step": 1,
                "name": "Collect No-Deposit Bonuses",
                "bookmakers": ["Betfair", "BetVictor", "Kambi"],
                "expected_value": "$50-100",
                "time": "1-2 days",
                "risk": "None",
            },
            {
                "step": 2,
                "name": "Run Arbitrage with Free Bets",
                "bookmakers": "Multiple",
                "expected_value": "$10-20 profit per $50 bonus",
                "time": "3-7 days",
                "risk": "None (arbitrage = 0% risk)",
            },
            {
                "step": 3,
                "name": "Use Profits for Deposit Matches",
                "bookmakers": "High-value promotions",
                "expected_value": "200-300% of initial bonus",
                "time": "7-14 days",
                "risk": "None (deploying your own profits)",
            },
            {
                "step": 4,
                "name": "Compound Growth",
                "bookmakers": "Multiple",
                "expected_value": "30-50% monthly return",
                "time": "30+ days",
                "risk": "Value betting risk (mitigated with Kelly Criterion)",
            },
        ]
