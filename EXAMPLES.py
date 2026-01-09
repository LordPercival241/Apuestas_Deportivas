"""
Examples and Documentation
Demonstrates system usage patterns and integrations
"""

# Example 1: Basic Event Processing
from main import BettingSystemOrchestrator
from config import DevelopmentConfig

# Initialize system
system = BettingSystemOrchestrator(DevelopmentConfig)
system.authenticate()

# Process a soccer event
system.process_event(event_id="evt_12345", sport="soccer")

# Example 2: Training the ML Model
from src.ml_models import MatchPredictor
import numpy as np

# Create predictor
predictor = MatchPredictor(model_type="gradient_boosting")

# Dummy training data
X_train = np.random.randn(100, 13)  # 13 features
y_train = np.random.randint(0, 2, 100)

# Train
predictor.train(X_train, y_train)

# Make prediction
match_data = {
    "home_form": 0.65,
    "away_form": 0.55,
    "home_possession_avg": 55,
    "away_possession_avg": 45,
    "injuries_home_count": 2,
    "injuries_away_count": 1,
}

prediction = predictor.predict_probability(match_data)
print(f"Home win probability: {prediction.get('home_win'):.2%}")

# Example 3: Bankroll Management with Kelly Criterion
from src.risk_management import BankrollManager

bankroll = BankrollManager(initial_bankroll=1000.0)

# Calculate optimal stake
stake = bankroll.calculate_optimal_stake(
    predicted_prob=0.65,
    decimal_odds=1.80,
    use_kelly=True
)

print(f"Recommended stake: ${stake:.2f}")

# Record bet result
bankroll.record_bet_result(stake=stake, result="won", winnings=stake * 0.80)
print(f"Current bankroll: ${bankroll.current_bankroll:.2f}")

# Example 4: Responsible Gaming Checks
from src.risk_management import ResponsibleGaming

gaming = ResponsibleGaming(pause_after_losses=3, max_daily_bets=20)

# Simulate loss streak
for i in range(3):
    should_pause = gaming.check_loss_streak("lost")
    if should_pause:
        print(f"System paused after {i+1} consecutive losses")
        break

# Example 5: Odds Comparison and Arbitrage Detection
from src.execution import ComparisonEngine

comparator = ComparisonEngine()

# Get best odds for a selection
best_odds = comparator.get_best_odds(
    event_id="evt_12345",
    market_id="match_odds",
    selection="home_win"
)

print(f"Best odds: {best_odds.get('best_odds')} on {best_odds.get('best_bookmaker')}")

# Detect arbitrage
outcomes = [
    {"selection": "home_win", "odds": 2.50},
    {"selection": "away_win", "odds": 1.60},
]

arbitrage = comparator.detect_arbitrage(outcomes)
if arbitrage and arbitrage.get("arbitrage_found"):
    print(f"Arbitrage found with {arbitrage.get('margin'):.2f}% margin")

# Example 6: Value Betting Analysis
from src.ml_models import ValueBettingCalculator, OddsConverter

# Convert odds
decimal_odds = 1.80
implied_prob = OddsConverter.decimal_to_probability(decimal_odds)
print(f"Implied probability of 1.80 odds: {implied_prob:.2%}")

# Calculate value
model_prob = 0.65
value = ValueBettingCalculator.calculate_value(model_prob, decimal_odds)
print(f"Value of this bet: {value:.2%}")

has_value = ValueBettingCalculator.has_value(model_prob, decimal_odds, min_threshold=0.05)
print(f"Has positive value: {has_value}")

# Example 7: Data Fetching
from src.data_acquisition import SportsDataFetcher

fetcher = SportsDataFetcher(api_key="your_api_key")

# Fetch live events
live_events = fetcher.fetch_live_events(sport="soccer")
print(f"Live soccer events: {len(live_events)}")

# Fetch historical data
history = fetcher.fetch_historical_data(team="Manchester United", limit=20)
print(f"Historical matches: {len(history)}")

# Example 8: Execution and Bet Placement
from src.execution import BetExecutor

executor = BetExecutor(bookmaker="betfair")
executor.authenticate(api_key="your_key", app_key="your_app_key")

bet_request = {
    "event_id": "evt_12345",
    "market_id": "match_odds",
    "selection": "home_win",
    "odds": 1.80,
    "stake": 25.0,
    "bet_type": "back",
}

confirmation = executor.place_bet(bet_request)
print(f"Bet placed: {confirmation.get('bet_id')}")

# Example 9: Audit and Compliance Logging
from src.utils import AuditLogger

audit = AuditLogger()

decision_log = {
    "event_id": "evt_12345",
    "prediction": {"home_win": 0.65, "confidence": 0.78},
    "odds": 1.80,
    "value": 0.17,
    "stake": 25.0,
    "action": "place_bet",
    "reason": "Positive value bet identified",
    "risk_metrics": {"bankroll_remaining": 1000.0, "daily_losses": 0.0},
}

audit.log_decision(decision_log)

# Example 10: Testing Value Betting Strategy
def test_value_betting_strategy():
    """
    Backtest a value betting strategy on historical data
    """
    import pandas as pd
    
    # Simulate 100 historical predictions
    results = {
        "event": range(100),
        "predicted_prob": np.random.uniform(0.5, 1.0, 100),
        "odds": np.random.uniform(1.5, 3.0, 100),
        "result": np.random.choice([0, 1], 100, p=[0.45, 0.55]),
    }
    
    df = pd.DataFrame(results)
    
    # Calculate value for each bet
    df["value"] = df.apply(
        lambda row: ValueBettingCalculator.calculate_value(row["predicted_prob"], row["odds"]),
        axis=1
    )
    
    # Filter value bets
    value_bets = df[df["value"] > 0.05]
    
    # Calculate ROI
    value_bets["return"] = value_bets["result"] * (value_bets["odds"] - 1) - (1 - value_bets["result"])
    roi = value_bets["return"].sum() / len(value_bets) if len(value_bets) > 0 else 0
    
    print(f"Value bets found: {len(value_bets)}")
    print(f"ROI on value bets: {roi:.2%}")
    print(f"Win rate: {value_bets['result'].mean():.2%}")
    
    return roi, value_bets

# Run example
# roi, bets = test_value_betting_strategy()
