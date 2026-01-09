#!/usr/bin/env python3
"""
Simple installation script that tests the project structure
"""
import sys
import subprocess

# Add the project to path
sys.path.insert(0, '.')

def test_imports():
    """Test if all modules can be imported"""
    print("[INFO] Testing module imports...\n")
    
    results = {
        "config": False,
        "data_acquisition": False,
        "ml_models": False,
        "execution": False,
        "risk_management": False,
        "utils": False
    }
    
    try:
        from config import current_config
        print("[OK] config module loaded")
        results["config"] = True
    except Exception as e:
        print(f"[ERROR] config: {e}")
    
    try:
        from src.data_acquisition import SportsDataFetcher
        print("[OK] data_acquisition module loaded")
        results["data_acquisition"] = True
    except Exception as e:
        print(f"[ERROR] data_acquisition: {e}")
    
    try:
        from src.ml_models import MatchPredictor
        print("[OK] ml_models module loaded")
        results["ml_models"] = True
    except Exception as e:
        print(f"[ERROR] ml_models: {e}")
    
    try:
        from src.execution import BetExecutor
        print("[OK] execution module loaded")
        results["execution"] = True
    except Exception as e:
        print(f"[ERROR] execution: {e}")
    
    try:
        from src.risk_management import BankrollManager
        print("[OK] risk_management module loaded")
        results["risk_management"] = True
    except Exception as e:
        print(f"[ERROR] risk_management: {e}")
    
    try:
        from src.utils import setup_logging
        print("[OK] utils module loaded")
        results["utils"] = True
    except Exception as e:
        print(f"[ERROR] utils: {e}")
    
    print("\n" + "="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Import Test Results: {passed}/{total} modules loaded successfully")
    print("="*60 + "\n")
    
    return all(results.values())

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
