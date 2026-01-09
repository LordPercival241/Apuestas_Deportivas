"""
Advanced Multi-Bet Arbitrage Examples
Demonstrates guaranteed profit and multiple bet strategies
"""

def example_three_way_arbitrage():
    """Example: Soccer match with home win, draw, away win"""
    from src.execution import ArbitrageEngine
    
    print("=" * 70)
    print("EXAMPLE 1: THREE-WAY ARBITRAGE (Soccer Match)")
    print("=" * 70)
    
    engine = ArbitrageEngine(min_profit_margin=0.01)
    
    # Real-world scenario: Different bookmakers offer different odds
    market_data = {
        "home_win": {
            "betfair": 2.50,
            "kambi": 2.45,
            "pinnacle": 2.48,
        },
        "draw": {
            "betfair": 3.40,
            "kambi": 3.20,
            "pinnacle": 3.35,
        },
        "away_win": {
            "betfair": 2.70,
            "kambi": 2.80,
            "pinnacle": 2.75,
        }
    }
    
    result = engine.find_market_arbitrage(market_data)
    
    if result and result["arbitrage_found"]:
        print(f"\n✅ ARBITRAGE FOUND!")
        print(f"   Outcomes: {result['outcomes']}")
        print(f"   Best odds: {result['best_odds']}")
        print(f"   Best bookmakers: {result['bookmakers']}")
        print(f"   Profit margin: {result['profit_margin_percent']:.2f}%")
        
        # Calculate optimal stakes for $1000 investment
        stakes = engine.calculate_arbitrage_stakes(
            total_bankroll=1000,
            odds_list=result['best_odds'],
            bookmakers=result['bookmakers'],
            outcomes=result['outcomes']
        )
        
        if stakes:
            print(f"\n   Total Investment: ${stakes['total_investment']:.2f}")
            print(f"   Guaranteed Profit: ${stakes['guaranteed_profit']:.2f}")
            print(f"   ROI: {stakes['roi_percent']:.2f}%")
            print(f"\n   Stake Distribution:")
            for outcome, details in stakes['stakes'].items():
                print(f"     - {outcome}: ${details['stake']:.2f} @ {details['odds']:.2f} ({details['bookmaker']})")
                print(f"       Returns: ${details['guaranteed_return']:.2f}")
    else:
        print("\n❌ No arbitrage found in this market")
    
    print()


def example_two_way_arbitrage():
    """Example: Tennis match - simple binary outcome"""
    from src.execution import ArbitrageEngine
    
    print("=" * 70)
    print("EXAMPLE 2: TWO-WAY ARBITRAGE (Tennis Match)")
    print("=" * 70)
    
    engine = ArbitrageEngine(min_profit_margin=0.01)
    
    # Betfair offers Player A at 1.95, Kambi offers Player B at 2.20
    odds_player_a = 1.95
    odds_player_b = 2.20
    
    is_arb, margin = engine.check_two_way_arbitrage(odds_player_a, odds_player_b)
    
    print(f"\nPlayer A odds: {odds_player_a} (Betfair)")
    print(f"Player B odds: {odds_player_b} (Kambi)")
    
    if is_arb:
        print(f"\n✅ ARBITRAGE FOUND!")
        print(f"   Profit margin: {margin*100:.2f}%")
        
        stakes = engine.calculate_arbitrage_stakes(
            total_bankroll=500,
            odds_list=[odds_player_a, odds_player_b],
            bookmakers=["Betfair", "Kambi"],
            outcomes=["Player A wins", "Player B wins"]
        )
        
        if stakes:
            print(f"\n   For $500 investment:")
            print(f"   Guaranteed Profit: ${stakes['guaranteed_profit']:.2f}")
            print(f"\n   Bet on Player A: ${stakes['stakes']['Player A wins']['stake']:.2f}")
            print(f"   Bet on Player B: ${stakes['stakes']['Player B wins']['stake']:.2f}")
    else:
        print(f"\n❌ No arbitrage: Sum of inverse odds = {1/odds_player_a + 1/odds_player_b:.4f}")
    
    print()


def example_parlay_optimization():
    """Example: Optimize multiple bets for maximum expected value"""
    from src.execution import MultiBetOptimizer
    
    print("=" * 70)
    print("EXAMPLE 3: MULTI-BET PARLAY OPTIMIZATION")
    print("=" * 70)
    
    optimizer = MultiBetOptimizer()
    
    # Three independent betting opportunities
    bets = [
        {
            "event": "Manchester vs Liverpool",
            "probability": 0.65,
            "odds": 1.80,
            "bookmaker": "Betfair"
        },
        {
            "event": "Real Madrid vs Barcelona",
            "probability": 0.70,
            "odds": 1.60,
            "bookmaker": "Kambi"
        },
        {
            "event": "Juventus vs Milan",
            "probability": 0.55,
            "odds": 2.10,
            "bookmaker": "Pinnacle"
        }
    ]
    
    print(f"\nAvailable bets:")
    for i, bet in enumerate(bets, 1):
        print(f"  {i}. {bet['event']}")
        print(f"     Probability: {bet['probability']:.1%} | Odds: {bet['odds']}")
    
    # Find best 2-bet combination for parlay
    best_combo = optimizer.find_best_combination(bets, combination_size=2)
    
    if best_combo:
        print(f"\n✅ BEST 2-BET PARLAY FOUND!")
        print(f"   Events: {[e['event'] for e in best_combo['events']]}")
        print(f"   Parlay Odds: {best_combo['parlay_odds']:.4f}")
        print(f"   Parlay Win Probability: {best_combo['parlay_probability']:.2%}")
        print(f"   Expected Value: +{best_combo['expected_value_percent']:.2f}%")
        print(f"   Recommendation: {best_combo['stake_recommendation']}")
    
    # Optimize allocation across all bets
    print(f"\n📊 OPTIMAL ALLOCATION FOR $1000 BANKROLL:")
    allocation = optimizer.optimize_multiple_bets(bets, bankroll=1000)
    
    for bet_key, bet_alloc in allocation['allocations'].items():
        if bet_alloc['stake'] > 0:
            print(f"\n{bet_alloc['event']}")
            print(f"  Stake: ${bet_alloc['stake']:.2f}")
            print(f"  Kelly %: {bet_alloc['kelly_percent']:.2f}%")
            print(f"  Expected Value: ${bet_alloc['expected_value']:.2f}")
    
    print(f"\nTotal Allocated: ${allocation['total_allocated']:.2f}")
    print(f"Remaining Bankroll: ${allocation['remaining_bankroll']:.2f}")
    print(f"Total Expected Value: ${allocation['total_expected_value']:.2f}")
    
    print()


def example_coverage_strategy():
    """Example: Cover all outcomes to guarantee return"""
    from src.execution import CoverageStrategy
    
    print("=" * 70)
    print("EXAMPLE 4: FULL COVERAGE STRATEGY (Guaranteed Return)")
    print("=" * 70)
    
    # Three possible outcomes with their odds
    outcomes = [
        {"name": "Home Win", "odds": 2.50},
        {"name": "Draw", "odds": 3.40},
        {"name": "Away Win", "odds": 2.70},
    ]
    
    bankroll = 1000
    
    result = CoverageStrategy.calculate_full_coverage(outcomes, bankroll)
    
    print(f"\nInvestment: ${bankroll:.2f}")
    print(f"Outcomes to cover:")
    for outcome in outcomes:
        print(f"  - {outcome['name']}: {outcome['odds']}")
    
    if result.get('is_arbitrage'):
        print(f"\n✅ ARBITRAGE AVAILABLE!")
        print(f"   Profit Margin: {result['profit_margin']*100:.2f}%")
    else:
        print(f"\n⚠️ No arbitrage, but covering all outcomes")
    
    print(f"\nStake Distribution:")
    for outcome_name, stake_info in result['stakes'].items():
        print(f"  {outcome_name}:")
        print(f"    Stake: ${stake_info['stake']:.2f}")
        print(f"    Returns: ${stake_info['return']:.2f}")
    
    print(f"\nGuaranteed Return on any outcome: ${result['guaranteed_return']:.2f}")
    
    print()


def example_hedging():
    """Example: Hedge an existing bet to lock in profits"""
    from src.execution import CoverageStrategy
    
    print("=" * 70)
    print("EXAMPLE 5: HEDGING STRATEGY (Lock Profits)")
    print("=" * 70)
    
    original_bet = {
        "odds": 3.5,
        "stake": 200,
        "description": "Manchester United to win at 3.5 odds"
    }
    
    target_profit = 200  # Lock in $200 profit regardless of outcome
    
    print(f"\nOriginal Bet:")
    print(f"  {original_bet['description']}")
    print(f"  Stake: ${original_bet['stake']:.2f}")
    print(f"  If wins: ${original_bet['stake'] * original_bet['odds']:.2f}")
    print(f"  If loses: $0")
    
    hedge = CoverageStrategy.calculate_hedging_stakes(original_bet, target_profit)
    
    if hedge:
        print(f"\n✅ HEDGING STRATEGY:")
        print(f"   Place opposing bet of: ${hedge['hedge_stake']:.2f}")
        print(f"   Result: Guaranteed profit of: ${hedge['guarantees_profit']:.2f}")
        print(f"   {hedge['note']}")
    
    print()


def main():
    """Run all examples"""
    print("\n")
    print("=" * 70)
    print(" ADVANCED MULTI-BET ARBITRAGE SYSTEM ".center(70))
    print("=" * 70)
    print("\n")
    
    try:
        example_three_way_arbitrage()
        example_two_way_arbitrage()
        example_parlay_optimization()
        example_coverage_strategy()
        example_hedging()
        
        print("=" * 70)
        print("ALL EXAMPLES COMPLETED")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
