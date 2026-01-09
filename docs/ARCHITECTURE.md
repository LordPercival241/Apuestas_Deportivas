"""
Architecture Documentation
Complete system design, data flows, and component interactions
"""

SYSTEM_ARCHITECTURE = """
╔════════════════════════════════════════════════════════════════════════════╗
║         SPORTS BETTING AUTONOMOUS SYSTEM - ARCHITECTURE                    ║
║                        v1.0.0 - January 2026                              ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. SYSTEM OVERVIEW                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flow:
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Real-time Events │────▶│ Data Acquisition │────▶│ Feature Extraction│
│ (Sportradar,     │     │ & Normalization  │     │ & Enrichment     │
│  Betfair APIs)   │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                           │
                                                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ ML PREDICTION LAYER                                              │
│ ┌─────────────────────────────────────────────────────────────┐  │
│ │ Model: Gradient Boosting / Logistic Regression             │  │
│ │ Input: 13+ features (form, injuries, possession, etc.)    │  │
│ │ Output: Probability distribution (Home/Draw/Away)          │  │
│ │ Confidence Score: 0-1 (minimum 60% for execution)          │  │
│ └─────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │ VALUE CALCULATION       │
                    │ Value = (P×O) - 1       │
                    │ Min threshold: +5%      │
                    └─────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────────────┐
                    │ RISK ASSESSMENT                 │
                    │ ├─ Kelly Criterion (1/4)        │
                    │ ├─ Daily loss limits (5%)       │
                    │ ├─ Bet count limits (20/day)    │
                    │ └─ Exposure checks              │
                    └─────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────────────┐
                    │ ODDS COMPARISON                 │
                    │ ├─ Betfair                      │
                    │ ├─ Kambi                        │
                    │ └─ Pinnacle                     │
                    └─────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────────────┐
                    │ EXECUTION DECISION              │
                    │ └─ Place Bet OR Skip            │
                    └─────────────────────────────────┘
                                │
                    ┌───────────┴────────────┐
                    ▼                        ▼
        ┌──────────────────────┐  ┌─────────────────┐
        │ PAPER TRADING        │  │ LIVE TRADING    │
        │ (Simulation)         │  │ (Real Bets)     │
        └──────────────────────┘  └─────────────────┘
                    │                        │
                    └───────────┬────────────┘
                                ▼
        ┌──────────────────────────────────────────┐
        │ AUDIT LOG & COMPLIANCE RECORDING         │
        │ ├─ Decision log                          │
        │ ├─ Responsible gaming alerts             │
        │ └─ Regulatory compliance                 │
        └──────────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │ OUTCOME SETTLEMENT & BANKROLL UPDATE     │
        │ ├─ Match final result                    │
        │ ├─ P&L calculation                       │
        │ └─ Model accuracy tracking               │
        └──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. COMPONENT ARCHITECTURE                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

A. DATA ACQUISITION MODULE (src/data_acquisition/)
   ├─ SportsDataFetcher
   │  ├─ Methods:
   │  │  ├─ fetch_live_events(sport) → List[Dict]
   │  │  ├─ fetch_event_odds(event_id) → Dict
   │  │  ├─ fetch_historical_data(team, limit) → DataFrame
   │  │  └─ _fetch_sportradar_events()
   │  │  └─ _fetch_betfair_events()
   │  └─ Providers: Sportradar, Betfair
   │
   └─ DataProcessor
      ├─ normalize_event_data() → Standardized format
      └─ enrich_event_with_context() → Add form, injuries, weather

B. ML MODELS MODULE (src/ml_models/)
   ├─ MatchPredictor
   │  ├─ Models: GradientBoostingClassifier, LogisticRegression
   │  ├─ Methods:
   │  │  ├─ extract_features(match_data) → np.ndarray
   │  │  ├─ train(X_train, y_train) → None
   │  │  ├─ predict_probability(match_data) → Dict
   │  │  ├─ save_model(filepath) → None
   │  │  └─ load_model(filepath) → None
   │  └─ Features: form, head-to-head, possession, shots, injuries
   │
   ├─ OddsConverter
   │  ├─ decimal_to_probability(odds) → float
   │  ├─ probability_to_decimal(prob) → float
   │  ├─ fractional_to_decimal(num, den) → float
   │  └─ american_to_decimal(odds) → float
   │
   └─ ValueBettingCalculator
      ├─ calculate_value(prob, odds) → float
      ├─ has_value(prob, odds, threshold) → bool
      └─ expected_value_units(stake, value) → float

C. EXECUTION MODULE (src/execution/)
   ├─ BetExecutor
   │  ├─ Bookmakers: Betfair, Kambi, Pinnacle
   │  ├─ Methods:
   │  │  ├─ authenticate(api_key, app_key) → bool
   │  │  ├─ validate_bet(bet_request) → bool
   │  │  ├─ place_bet(bet_request) → Dict
   │  │  ├─ cancel_bet(bet_id) → bool
   │  │  └─ get_bet_status(bet_id) → Dict
   │  └─ BetStatus enum: PENDING, ACCEPTED, REJECTED, MATCHED, WON, LOST
   │
   └─ ComparisonEngine
      ├─ get_best_odds(event_id, market_id, selection) → Dict
      └─ detect_arbitrage(outcomes) → Optional[Dict]

D. RISK MANAGEMENT MODULE (src/risk_management/)
   ├─ BankrollManager
   │  ├─ Attributes:
   │  │  ├─ current_bankroll: float
   │  │  ├─ daily_losses: float
   │  │  └─ max_single_bet_percent: float
   │  ├─ Methods:
   │  │  ├─ kelly_criterion(win_prob, odds) → float (0-0.25)
   │  │  ├─ calculate_optimal_stake(prob, odds) → float
   │  │  ├─ record_bet_result(stake, result, winnings) → None
   │  │  └─ check_bankroll_health() → RiskLevel
   │  └─ Formulas:
   │     ├─ Kelly: (bp - q) / b
   │     └─ Fractional Kelly: Kelly / 4
   │
   ├─ ResponsibleGaming
   │  ├─ Methods:
   │  │  ├─ check_loss_streak(result) → bool
   │  │  ├─ check_daily_limits(current_bets) → bool
   │  │  └─ get_pause_duration() → timedelta
   │  └─ Pauses: After 3 consecutive losses (configurable)
   │
   └─ ExposureManager
      ├─ max_exposure_per_sport: 10%
      ├─ max_exposure_per_team: 5%
      └─ add_exposure(), check_exposure_limits()

E. UTILITIES & COMPLIANCE (src/utils.py)
   ├─ setup_logging() → logger (rotating file handlers)
   ├─ AuditLogger
   │  ├─ log_decision(decision) → None
   │  └─ log_error(error_type, details) → None
   ├─ DatabaseManager (PostgreSQL)
   │  └─ Methods: connect(), save_event(), save_bet(), save_prediction()
   └─ ArchitectureDocumentation

┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. DATA STRUCTURES                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

Event Data:
{
    "event_id": "evt_12345",
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "sport": "soccer",
    "status": "live",
    "home_score": 1,
    "away_score": 0,
    "timestamp": "2026-01-05T18:30:00Z",
    "home_form": [1, 1, 0, 1, 1],  # Last 5 results
    "away_form": [1, 0, 1, 0, 1],
    "injuries": ["player1", "player2"],
    "possession_home": 55,
    "possession_away": 45,
}

Prediction Output:
{
    "home_win": 0.62,
    "draw": 0.18,
    "away_win": 0.20,
    "confidence": 0.78,
}

Bet Request:
{
    "event_id": "evt_12345",
    "market_id": "match_odds",
    "selection": "home_win",
    "odds": 1.80,
    "stake": 25.00,
    "bet_type": "back",
}

Audit Log Entry:
{
    "timestamp": "2026-01-05T18:35:00Z",
    "event_id": "evt_12345",
    "model_prediction": {"home_win": 0.62, "confidence": 0.78},
    "market_odds": 1.80,
    "calculated_value": 0.116,  # +11.6%
    "stake": 25.00,
    "decision": "place_bet",
    "reason": "Positive value bet with >60% confidence",
    "risk_metrics": {"bankroll_remaining": 1000.0, "daily_losses": 0.0},
}

┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. DATABASE SCHEMA (PostgreSQL)                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Tables:
├─ betting.events
│  └─ event_id, sport, home_team, away_team, status, home_score, away_score
├─ betting.odds
│  └─ odds_id, event_id, bookmaker, market_type, selection, decimal_odds
├─ betting.predictions
│  └─ prediction_id, event_id, home_win_prob, draw_prob, away_win_prob, confidence
├─ betting.bets
│  └─ bet_id, event_id, stake, odds, status, result, profit_loss
├─ betting.bankroll_history
│  └─ bankroll_amount, daily_pnl, recorded_at
├─ betting.audit_log
│  └─ log_id, event_id, action, decision, confidence, created_at
├─ betting.model_performance
│  └─ model_name, accuracy, precision, recall, f1_score, roi
└─ betting.gaming_alerts
   └─ alert_id, alert_type, consecutive_losses, created_at

┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. PROCESSING PIPELINE EXECUTION                                            │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: EVENT INGESTION (Real-time)
├─ Fetch from Sportradar/Betfair every 10 seconds
├─ Normalize to standard schema
└─ Store in PostgreSQL events table

Step 2: FEATURE EXTRACTION
├─ Calculate team form (weighted avg last 5 matches)
├─ Fetch injury reports
├─ Get head-to-head statistics
├─ Retrieve possession and shot data
└─ Estimate weather impact

Step 3: MODEL INFERENCE
├─ Load trained model from disk
├─ Scale features with fitted scaler
├─ Generate probability predictions
├─ Calculate confidence score
└─ Validation: confidence > 60%?

Step 4: VALUE ANALYSIS
├─ Fetch market odds from multiple bookmakers
├─ Calculate implied probability from odds
├─ Compute value: (P × O) - 1
├─ Validation: value > 5%?
└─ Find best odds among bookmakers

Step 5: RISK ASSESSMENT
├─ Calculate Kelly fraction: (bp - q) / b → 1/4 Kelly
├─ Determine optimal stake based on bankroll
├─ Check daily loss limits (5% max)
├─ Check daily bet count (20 max)
├─ Verify loss streak (pause after 3)
└─ Check exposure limits per sport/team

Step 6: DECISION MAKING
├─ All criteria met?
│  ├─ YES → Place bet (or paper trade)
│  └─ NO → Log and skip
└─ Log decision with full audit trail

Step 7: EXECUTION
├─ Authenticate with bookmaker
├─ Validate bet parameters
├─ Send bet order
└─ Receive confirmation/bet_id

Step 8: MONITORING
├─ Poll bet status
├─ Track live odds movement
├─ Calculate current P&L
└─ Watch for alerts

Step 9: SETTLEMENT
├─ Match concludes
├─ Fetch final result
├─ Settle bet
├─ Update bankroll
└─ Record outcome

Step 10: ANALYTICS
├─ Calculate accuracy metrics
├─ Update model performance stats
├─ Track ROI and Sharpe ratio
└─ Identify model drift

┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. API INTEGRATIONS                                                         │
└─────────────────────────────────────────────────────────────────────────────┘

SPORTRADAR API
├─ Base: https://api.sportradar.com/soccer/
├─ Endpoints:
│  ├─ /events (live matches)
│  ├─ /matches/{id}/statistics
│  ├─ /teams/{id}/form
│  └─ /injuries
├─ Rate limit: 10,000 requests/day
└─ Authentication: API key in query params

BETFAIR API
├─ Base: https://api.betfair.com/exchange/betting/
├─ Methods:
│  ├─ listEvents()
│  ├─ listMarketCatalogue()
│  ├─ listMarketBook()
│  ├─ placeOrders()
│  └─ listCurrentOrders()
├─ Rate limit: 50 requests/sec
└─ Authentication: Session token from login

┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. DEPLOYMENT ARCHITECTURE                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Production Deployment:
┌────────────────────────────────────────────────────────────────┐
│                      CLOUD INFRASTRUCTURE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐  │
│  │   API Endpoints  │  │  Data Ingestion  │  │   ML Model  │  │
│  │   (Flask/REST)   │  │    (Celery)      │  │ Inference   │  │
│  └──────────────────┘  └──────────────────┘  └─────────────┘  │
│            │                    │                     │         │
│            └────────────────────┼─────────────────────┘         │
│                                 ▼                               │
│                    ┌──────────────────────┐                    │
│                    │  Message Queue       │                    │
│                    │  (RabbitMQ/Redis)    │                    │
│                    └──────────────────────┘                    │
│                                 │                               │
│  ┌──────────────────────────────┼──────────────────────────┐  │
│  ▼                              ▼                          ▼   │
│ ┌────────────────┐  ┌─────────────────────┐  ┌──────────────┐ │
│ │  PostgreSQL    │  │  Redis Cache        │  │ Audit Logs   │ │
│ │  (Events,      │  │  (Predictions,      │  │  (Files)     │ │
│ │   Bets, etc.)  │  │   Odds)             │  │              │ │
│ └────────────────┘  └─────────────────────┘  └──────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. SECURITY & COMPLIANCE                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Security Measures:
├─ Environment variables for API keys
├─ SSL/TLS for all external communications
├─ Session token management
├─ Input validation and sanitization
├─ Rate limiting on API calls
└─ Encrypted password storage

Compliance:
├─ GDPR: User data protection, right to deletion
├─ KYC/AML: Identity verification
├─ Age verification: 18+ requirement
├─ Geolocation: Restricted regions check
├─ Responsible gaming: Mandatory safeguards
└─ Audit trail: Complete decision logging

┌─────────────────────────────────────────────────────────────────────────────┐
│ 9. PERFORMANCE METRICS                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

System KPIs:
├─ Event processing latency: <1 second
├─ Model inference time: <500ms
├─ Bet placement latency: <2 seconds
├─ API availability: >99.5%
├─ Data accuracy: >95%
└─ Model accuracy: Target >55% (better than random)

Model Metrics:
├─ Precision: TP / (TP + FP)
├─ Recall: TP / (TP + FN)
├─ F1 Score: 2 × (P × R) / (P + R)
├─ ROI: (Profit / Total Stake) × 100
└─ Sharpe Ratio: (Return - Risk-free rate) / Volatility

┌─────────────────────────────────────────────────────────────────────────────┐
│ 10. FUTURE ENHANCEMENTS                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 2:
├─ Web dashboard (React.js)
├─ Mobile app (iOS/Android)
├─ Ensemble models (multiple models voting)
├─ Transfer learning from related sports
└─ Real-time odds streaming (WebSockets)

Phase 3:
├─ Blockchain-based audit trail
├─ Smart contracts for automated settlement
├─ Decentralized betting
├─ Multi-user support with role-based access
└─ Advanced analytics dashboard

Phase 4:
├─ AI-powered lineup analysis
├─ Sentiment analysis from news/social media
├─ Player-level performance modeling
├─ In-play betting with live updates
└─ Advanced arbitrage detection
"""

# System design principles:
print(SYSTEM_ARCHITECTURE)
