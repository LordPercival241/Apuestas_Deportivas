"""
Main Application Entry Point
Orchestrates all system components
"""
import logging
from datetime import datetime
from config import current_config
from src.data_acquisition import SportsDataFetcher, DataProcessor
from src.ml_models import MatchPredictor, ValueBettingCalculator
from src.execution import BetExecutor, ComparisonEngine
from src.risk_management import BankrollManager, ResponsibleGaming
from src.utils import setup_logging, AuditLogger

class BettingSystemOrchestrator:
    """
    Main orchestrator that coordinates all system components
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging(config.LOG_LEVEL)
        self.audit_logger = AuditLogger()
        
        # Initialize components
        self.data_fetcher = SportsDataFetcher(
            api_key=config.SPORTRADAR_API_KEY,
            provider="sportradar"
        )
        self.data_processor = DataProcessor()
        self.predictor = MatchPredictor(model_type="gradient_boosting")
        self.executor = BetExecutor(
            bookmaker="betfair",
            username=config.BETFAIR_USERNAME,
            password=config.BETFAIR_PASSWORD
        )
        self.comparison_engine = ComparisonEngine()
        self.bankroll_manager = BankrollManager(
            initial_bankroll=config.BANKROLL_INITIAL,
            max_daily_loss_percent=config.MAX_DAILY_LOSS_PERCENT,
            max_single_bet_percent=config.MAX_SINGLE_BET_PERCENT
        )
        self.responsible_gaming = ResponsibleGaming(
            pause_after_losses=config.PAUSE_AFTER_LOSS_STREAK,
            max_daily_bets=config.MAX_BETS_PER_DAY
        )
    
    def authenticate(self) -> bool:
        """Authenticate with bookmaker APIs"""
        try:
            self.executor.authenticate(
                api_key=self.config.BETFAIR_APP_KEY,
                app_key=self.config.BETFAIR_APP_KEY
            )
            self.logger.info("System authentication successful")
            return True
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def process_event(self, event_id: str, sport: str = "soccer") -> None:
        """
        Process a single sporting event
        
        Flow:
        1. Fetch event and odds data
        2. Get historical context
        3. Extract features and make prediction
        4. Compare odds across bookmakers
        5. Evaluate value and risk
        6. Execute bet if criteria met
        """
        try:
            # Step 1: Fetch data
            live_events = self.data_fetcher.fetch_live_events(sport=sport)
            if not live_events:
                self.logger.warning(f"No live events found for {sport}")
                return
            
            event = next((e for e in live_events if e.get("event_id") == event_id), None)
            if not event:
                self.logger.warning(f"Event {event_id} not found")
                return
            
            # Process event data
            processed_event = self.data_processor.normalize_event_data(event)
            
            # Step 2: Get historical data
            historical_data = self.data_fetcher.fetch_historical_data(
                team=processed_event.get("home_team"),
                limit=50
            )
            
            # Step 3: Make prediction
            enriched_event = self.data_processor.enrich_event_with_context(
                processed_event,
                historical_data
            )
            
            prediction = self.predictor.predict_probability(enriched_event)
            if not prediction:
                self.logger.warning(f"Prediction failed for event {event_id}")
                return
            
            # Check confidence threshold
            if prediction.get("confidence", 0) < self.config.MIN_CONFIDENCE_THRESHOLD:
                self.logger.info(f"Event {event_id}: Confidence too low ({prediction.get('confidence')})")
                return
            
            # Step 4: Compare odds
            odds_data = self.data_fetcher.fetch_event_odds(event_id)
            best_odds = self.comparison_engine.get_best_odds(
                event_id=event_id,
                market_id="match_odds",
                selection="home_win"
            )
            
            # Step 5: Calculate value
            value = ValueBettingCalculator.calculate_value(
                predicted_prob=prediction.get("home_win", 0),
                decimal_odds=best_odds.get("best_odds", 1.0)
            )
            
            if not ValueBettingCalculator.has_value(
                prediction.get("home_win", 0),
                best_odds.get("best_odds", 1.0),
                min_threshold=0.05
            ):
                self.logger.info(f"Event {event_id}: No positive value found")
                return
            
            # Step 6: Risk check and execution
            stake = self.bankroll_manager.calculate_optimal_stake(
                predicted_prob=prediction.get("home_win", 0),
                decimal_odds=best_odds.get("best_odds", 1.0),
                use_kelly=True
            )
            
            if stake <= 0:
                self.logger.warning(f"Event {event_id}: Stake calculation resulted in zero")
                return
            
            # Check responsible gaming limits
            if not self.responsible_gaming.check_daily_limits(self.responsible_gaming.daily_bet_count):
                self.logger.warning("Daily bet limit reached")
                return
            
            # Final decision
            decision = {
                "event_id": event_id,
                "prediction": prediction,
                "odds": best_odds.get("best_odds"),
                "value": value,
                "stake": stake,
                "action": "place_bet",
                "reason": f"Value bet detected: {value*100:.2f}%",
                "risk_metrics": {
                    "bankroll_remaining": self.bankroll_manager.current_bankroll,
                    "daily_losses": self.bankroll_manager.daily_losses,
                },
            }
            
            # Log decision
            self.audit_logger.log_decision(decision)
            
            # Execute bet if in live mode
            if not self.config.PAPER_TRADING and self.config.LIVE_TRADING:
                bet_request = {
                    "event_id": event_id,
                    "market_id": "match_odds",
                    "selection": "home_win",
                    "odds": best_odds.get("best_odds"),
                    "stake": stake,
                    "bet_type": "back",
                }
                
                confirmation = self.executor.place_bet(bet_request)
                self.logger.info(f"Bet placed: {confirmation}")
            else:
                self.logger.info(f"Paper trading - Bet would be placed: {stake} at {best_odds.get('best_odds')}")
        
        except Exception as e:
            self.logger.error(f"Error processing event {event_id}: {str(e)}")
            self.audit_logger.log_error("event_processing", {"event_id": event_id, "error": str(e)})

def main():
    """Main application entry point"""
    print("=" * 60)
    print("Sports Betting Autonomous System v1.0.0")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Mode: {'PAPER TRADING' if current_config.PAPER_TRADING else 'LIVE TRADING'}")
    print(f"Bankroll: ${current_config.BANKROLL_INITIAL}")
    print(f"Environment: {current_config.ENVIRONMENT}")
    print("=" * 60)
    
    # Initialize system
    system = BettingSystemOrchestrator(current_config)
    
    # Authenticate
    if not system.authenticate():
        print("ERROR: Authentication failed. Exiting.")
        return
    
    print("✓ System initialized and authenticated")
    print("✓ Ready for event processing")
    print("\nSystem Components:")
    print("  - Data Acquisition: Real-time event fetching")
    print("  - ML Models: Predictive analysis")
    print("  - Execution: Automated bet placement")
    print("  - Risk Management: Bankroll protection")
    print("=" * 60)

if __name__ == "__main__":
    main()
