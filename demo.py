"""
Demo Script - Sports Betting System
Demonstrates Kelly Criterion, Value Betting, and Bankroll Management
"""

def demo_kelly_criterion():
    """Demonstrate Kelly Criterion calculation"""
    from src.risk_management import BankrollManager
    
    print("=" * 60)
    print("KELLY CRITERION EXAMPLE")
    print("=" * 60)
    
    bm = BankrollManager(1000.0, max_daily_loss_percent=5.0, max_single_bet_percent=2.0)
    
    print(f"Predicted probability: 65%")
    print(f"Market odds: 1.80")
    
    kelly = bm.kelly_criterion(0.65, 1.80)
    print(f"Kelly fraction: {kelly:.4f} ({kelly*100:.2f}%)")
    
    stake = bm.calculate_optimal_stake(0.65, 1.80, use_kelly=True)
    print(f"Optimal stake: ${stake:.2f}")
    
    print()

def demo_value_betting():
    """Demonstrate Value Betting calculation"""
    from src.ml_models import ValueBettingCalculator, OddsConverter
    
    print("=" * 60)
    print("VALUE BETTING ANALYSIS")
    print("=" * 60)
    
    prob = 0.65
    odds = 1.80
    
    value = ValueBettingCalculator.calculate_value(prob, odds)
    implied_prob = OddsConverter.decimal_to_probability(odds)
    
    print(f"Predicted probability: {prob:.1%}")
    print(f"Market odds: {odds}")
    print(f"Implied probability from odds: {implied_prob:.1%}")
    print(f"Calculated value: {value:.1%}")
    print(f"Has positive value (>5%): {ValueBettingCalculator.has_value(prob, odds, 0.05)}")
    
    print()

def demo_bankroll_management():
    """Demonstrate Bankroll Management"""
    from src.risk_management import BankrollManager
    
    print("=" * 60)
    print("BANKROLL SIMULATION")
    print("=" * 60)
    
    bm = BankrollManager(1000.0)
    print(f"Initial bankroll: ${bm.current_bankroll:.2f}")
    print()
    
    # Simulate some bets
    bets = [
        ("won", 50.0, 40.0),
        ("won", 75.0, 60.0),
        ("lost", 100.0, 0.0),
        ("won", 80.0, 64.0),
        ("lost", 60.0, 0.0),
    ]
    
    for i, (result, stake, winnings) in enumerate(bets, 1):
        bm.record_bet_result(stake, result, winnings)
        status = f"WON (${winnings:.0f})" if result == "won" else f"LOST (${stake:.0f})"
        print(f"Bet {i}: {status} -> Bankroll: ${bm.current_bankroll:.2f}")
    
    print()
    print(f"Total daily losses: ${bm.daily_losses:.2f}")
    print(f"Bankroll health: {bm.check_bankroll_health().value}")
    print()

def demo_responsible_gaming():
    """Demonstrate Responsible Gaming Safeguards"""
    from src.risk_management import ResponsibleGaming
    
    print("=" * 60)
    print("RESPONSIBLE GAMING - LOSS STREAK DETECTION")
    print("=" * 60)
    
    rg = ResponsibleGaming(pause_after_losses=3, max_daily_bets=20)
    
    results = ["lost", "lost", "lost"]  # 3 consecutive losses
    
    for i, result in enumerate(results, 1):
        should_pause = rg.check_loss_streak(result)
        print(f"Bet {i}: {result.upper()} (Consecutive losses: {rg.consecutive_losses})")
        
        if should_pause:
            print(f"  --> SYSTEM PAUSED after {rg.consecutive_losses} consecutive losses")
            print(f"  --> Pause duration: {rg.get_pause_duration()}")
    
    print()

def demo_model_prediction():
    """Demonstrate ML Model Prediction"""
    from src.ml_models import MatchPredictor
    import numpy as np
    
    print("=" * 60)
    print("ML MODEL PREDICTION EXAMPLE")
    print("=" * 60)
    
    predictor = MatchPredictor(model_type="logistic_regression")
    
    # Train with dummy data
    X_train = np.random.randn(50, 13)
    y_train = np.random.randint(0, 2, 50)
    predictor.train(X_train, y_train)
    print("Model trained successfully")
    
    # Make prediction
    match_data = {
        "home_form": 0.68,
        "away_form": 0.52,
        "home_possession_avg": 56,
        "away_possession_avg": 44,
        "injuries_home_count": 1,
        "injuries_away_count": 2,
        "home_shots_avg": 5,
        "away_shots_avg": 3,
    }
    
    prediction = predictor.predict_probability(match_data)
    print(f"\nMatch: Manchester United vs Liverpool")
    print(f"Home win probability: {prediction.get('home_win', 0):.1%}")
    print(f"Draw probability: {prediction.get('draw', 0):.1%}")
    print(f"Away win probability: {prediction.get('away_win', 0):.1%}")
    print(f"Confidence score: {prediction.get('confidence', 0):.1%}")
    print()

def demo_odds_comparison():
    """Demonstrate Odds Comparison and Arbitrage Detection"""
    from src.execution import ComparisonEngine
    
    print("=" * 60)
    print("ODDS COMPARISON & ARBITRAGE DETECTION")
    print("=" * 60)
    
    comparator = ComparisonEngine()
    
    # Example: Compare odds for home win
    odds_data = comparator.get_best_odds(
        event_id="evt_12345",
        market_id="match_odds",
        selection="home_win"
    )
    
    print(f"Selection: {odds_data.get('selection')}")
    print(f"Best odds: {odds_data.get('best_odds')} on {odds_data.get('best_bookmaker')}")
    print(f"\nOdds across bookmakers:")
    for bookmaker, odds in odds_data.get('available_odds', {}).items():
        print(f"  {bookmaker}: {odds}")
    
    print()
    
    # Detect arbitrage
    outcomes = [
        {"selection": "home_win", "odds": 2.50},
        {"selection": "away_win", "odds": 1.60},
    ]
    
    arbitrage = comparator.detect_arbitrage(outcomes)
    if arbitrage and arbitrage.get("arbitrage_found"):
        print(f"Arbitrage opportunity found!")
        print(f"Margin: {arbitrage.get('margin'):.2f}%")
    else:
        print("No arbitrage opportunities detected")
    
    print()

def main():
    """Run all demos"""
    print("\n")
    print("=" * 60)
    print(" SPORTS BETTING AUTONOMOUS SYSTEM - DEMONSTRATION ".center(60))
    print("=" * 60)
    print("\n")
    
    try:
        demo_kelly_criterion()
        demo_value_betting()
        demo_bankroll_management()
        demo_responsible_gaming()
        demo_model_prediction()
        demo_odds_comparison()
        
        print("=" * 60)
        print("DEMO COMPLETE")
        print("=" * 60)
        print("\nAll system components working correctly!")
        print("\nNext steps:")
        print("1. Configure .env file with API keys")
        print("2. Set up PostgreSQL database")
        print("3. Train ML models with historical data")
        print("4. Run backtests to validate strategy")
        print("5. Deploy in paper trading mode")
        print("6. Monitor performance before live trading")
        
    except Exception as e:
        print(f"Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
