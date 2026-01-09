# Sports Betting Autonomous System

A comprehensive Python system for real-time sports event monitoring, predictive analysis, and automated betting execution with robust risk management and ethical safeguards.

## Project Structure

```
sports-betting-system/
├── src/
│   ├── data_acquisition/      # Real-time data fetching from APIs
│   ├── ml_models/             # Predictive models and odds analysis
│   ├── execution/             # Automated bet placement
│   ├── risk_management/       # Bankroll and safety management
│   ├── dashboard/             # Control panel (future)
│   └── utils.py               # Logging and utilities
├── database/
│   └── schema.sql             # PostgreSQL schema
├── tests/                     # Unit and integration tests
├── docs/                      # Architecture and API documentation
├── main.py                    # System orchestrator
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Key Components

### 1. Data Acquisition Module
- **Real-time monitoring** of sporting events
- **Multi-source integration**: Sportradar, Betfair APIs
- **Data normalization** and standardization
- **Historical data** retrieval and storage

### 2. Machine Learning Models
- **Match outcome prediction** using Gradient Boosting and Logistic Regression
- **Feature extraction** from team form, injuries, weather, etc.
- **Probability calculation** with confidence scoring
- **Model persistence** (save/load trained models)

### 3. Execution Module
- **Secure authentication** with betting platforms
- **Automated bet placement** with validation
- **Odds comparison** across multiple bookmakers
- **Arbitrage detection** for risk-free opportunities

### 4. Risk Management
- **Kelly Criterion** for optimal stake sizing
- **Bankroll protection** with daily/weekly limits
- **Loss streak detection** (pause after N consecutive losses)
- **Exposure management** per sport/team
- **Responsible gaming** safeguards

### 5. Compliance & Audit
- **Detailed decision logging** for transparency
- **Regulatory compliance** (GDPR, KYC/AML)
- **Geolocation checks** and age verification
- **Audit trail** of all bets and decisions

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (for data storage)
- Redis (optional, for caching)

### Setup

1. **Clone and install dependencies:**
```bash
cd sports-betting-system
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

3. **Setup database:**
```bash
psql -U postgres -f database/schema.sql
```

4. **Train ML models (optional):**
```bash
python scripts/train_model.py
```

## Usage

### Basic Usage
```python
from main import BettingSystemOrchestrator
from config import DevelopmentConfig

# Initialize
system = BettingSystemOrchestrator(DevelopmentConfig)
system.authenticate()

# Process events
system.process_event(event_id="evt_12345", sport="soccer")
```

### Paper Trading
Enable `PAPER_TRADING=True` in `.env` to simulate bets without actual execution.

### Live Trading
Set `LIVE_TRADING=True` after thorough testing and backtesting.

## Risk Management Features

### Kelly Criterion
Optimal stake calculation: `Kelly% = (bp - q) / b`
- Fractional Kelly (1/4 Kelly) used for safety
- Maximum single bet capped at 25% of bankroll

### Daily Limits
- Maximum daily loss: 5% of bankroll (configurable)
- Maximum bets per day: 20 (configurable)
- Loss streak pause: 3 consecutive losses triggers 1-hour pause

### Exposure Limits
- Maximum 10% of bankroll per sport
- Maximum 5% of bankroll per team

## APIs and Integrations

### Supported Data Providers
1. **Sportradar** - Live event and stats
2. **Betfair** - Odds and liquidity

### Supported Bookmakers
1. **Betfair** - High liquidity, lay betting
2. **Kambi** - European coverage
3. **Pinnacle** - Competitive odds

## Model Performance Metrics

System tracks:
- **Accuracy**: Percentage of correct predictions
- **Precision**: True positives / (true positives + false positives)
- **Recall**: True positives / (true positives + false negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **ROI**: Return on investment of placed bets
- **Sharpe Ratio**: Risk-adjusted returns

## Testing and Backtesting

### Unit Tests
```bash
pytest tests/
```

### Backtesting
```bash
python scripts/backtest.py --start_date 2023-01-01 --end_date 2023-12-31
```

## Security Considerations

1. **API Key Management**: Use environment variables, never hardcode
2. **Encryption**: All sensitive data encrypted at rest and in transit
3. **Authentication**: Secure session tokens with bookmakers
4. **Rate Limiting**: Respect API rate limits
5. **Input Validation**: All inputs sanitized before processing

## Responsible Gaming

The system includes mandatory safeguards:
- Loss streak detection and automatic pause
- Daily betting limits
- Bankroll protection mechanisms
- Geolocation verification
- Age verification
- Responsible gaming alerts

## Compliance Requirements

- ✅ GDPR compliance (EU)
- ✅ KYC/AML verification
- ✅ Age 18+ verification
- ✅ Geolocation restrictions
- ✅ Audit logging
- ✅ Decision explainability

## Ethical Guidelines

This system operates under strict ethical principles:

1. **Transparency**: All betting decisions logged and explainable
2. **Integrity**: No manipulation of odds or data
3. **Fairness**: Bets placed fairly without exploitative tactics
4. **Responsible Gambling**: Safeguards for problem gambling
5. **Legal Compliance**: Operates within all applicable regulations

## Performance Optimization

- Real-time event processing with <1 second latency
- Batch prediction processing
- Redis caching for frequently accessed data
- Database query optimization with indexes
- Model inference optimization (ONNX export)

## Monitoring and Alerts

The system provides real-time monitoring of:
- Active bets and P&L
- Bankroll status
- Model accuracy and ROI
- System health and errors
- Compliance alerts

## Future Enhancements

- [ ] Web dashboard with real-time updates
- [ ] Mobile app for monitoring
- [ ] Additional sports (tennis, basketball, etc.)
- [ ] Advanced ensemble models
- [ ] Blockchain-based audit trail
- [ ] Multi-user support

## Documentation

See `docs/` folder for:
- `ARCHITECTURE.md` - System design and data flow
- `API.md` - API documentation
- `RISK_MANAGEMENT.md` - Risk management strategies
- `COMPLIANCE.md` - Regulatory and ethical framework

## Contributing

Contributions are welcome! Please ensure:
1. Unit tests pass
2. Code follows PEP8 style guide
3. Documentation is updated
4. Risk management features preserved

## License

This project is licensed under the MIT License - see LICENSE file.

## Support

For issues or questions:
- Create an issue on GitHub
- Check documentation in `docs/`
- Review examples in `EXAMPLES.py`

## Disclaimer

⚠️ **IMPORTANT**: Sports betting involves financial risk. This system is provided for educational purposes. Users are responsible for:
- Compliance with local gambling laws
- Understanding the risks of sports betting
- Responsible gambling practices
- All financial losses

Always test thoroughly in paper trading mode before live deployment.

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Status**: Production Ready (with proper testing)
