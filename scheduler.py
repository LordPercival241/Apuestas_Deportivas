"""
Scheduler para ejecutar el bot de apuestas automáticamente
Ejecuta cada cierto tiempo para monitorear oportunidades
"""
import schedule
import time
import logging
from datetime import datetime
from main import BettingSystemOrchestrator
from config import current_config
from src.utils import setup_logging

logger = setup_logging(current_config.LOG_LEVEL)


def run_bot_cycle():
    """
    Ejecutar un ciclo completo del bot
    """
    try:
        logger.info("=" * 60)
        logger.info(f"Starting bot cycle at {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Inicializar sistema
        system = BettingSystemOrchestrator(current_config)
        
        # Autenticar
        if not system.authenticate():
            logger.error("Authentication failed")
            return False
        
        logger.info("System authenticated successfully")
        logger.info("System initialized and ready for event processing")
        
        # Aquí iría la lógica de procesamiento de eventos
        # system.process_events()
        
        logger.info("Bot cycle completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during bot cycle: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def schedule_bot():
    """
    Programar ejecuciones del bot
    """
    # Ejecutar cada 6 horas
    schedule.every(6).hours.do(run_bot_cycle)
    
    # Ejecutar cada día a las 0:00 UTC
    schedule.every().day.at("00:00").do(run_bot_cycle)
    
    # Ejecutar cada día a las 12:00 UTC
    schedule.every().day.at("12:00").do(run_bot_cycle)
    
    logger.info("Bot scheduler started")
    logger.info("Schedule:")
    logger.info("  - Every 6 hours")
    logger.info("  - Daily at 00:00 UTC")
    logger.info("  - Daily at 12:00 UTC")


def main():
    """
    Punto de entrada para el scheduler
    """
    print("=" * 60)
    print("Sports Betting Autonomous System - Scheduler")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")
    print(f"Configuration: {current_config.ENVIRONMENT}")
    print(f"Paper Trading: {current_config.PAPER_TRADING}")
    print(f"Live Trading: {current_config.LIVE_TRADING}")
    print("=" * 60)
    
    # Programar el bot
    schedule_bot()
    
    # Ejecutar scheduler indefinidamente
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Revisar cada minuto
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            time.sleep(300)  # Esperar 5 minutos antes de reintentar


if __name__ == "__main__":
    main()
