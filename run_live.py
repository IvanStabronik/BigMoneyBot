import time
import queue
import MetaTrader5 as mt5
from src.core.event_bus import EventBus
from src.core.events import EventType
from src.data.mt5_data_handler import MT5DataHandler
from src.strategy.smc_strategy import SMCStrategy
from src.portfolio.portfolio import Portfolio
from src.execution.mt5_execution import MT5ExecutionHandler
from src.db.database import init_db, get_session
from src.db.models import TradeRecord
from src.utils.logger import logger
from src.utils.config import config

def run_trading_system():
    logger.info("Initializing Enterprise SMC Trading System...")
    
    # Init DB
    init_db()
    
    # Init MT5
    if not mt5.initialize():
        logger.error("Failed to initialize MT5")
        return
        
    logger.info("MT5 Initialized Successfully")

    # Core components
    event_bus = EventBus()
    data_handler = MT5DataHandler(event_bus)
    strategy = SMCStrategy(event_bus)
    portfolio = Portfolio(event_bus)
    execution = MT5ExecutionHandler(event_bus)

    logger.info("Starting main event loop...")
    try:
        while True:
            # 1. Fetch new market data
            data_handler.update_bars()

            # 2. Process all events in the queue
            while True:
                try:
                    event = event_bus.get(block=False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == EventType.MARKET:
                            strategy.calculate_signals(event)
                        elif event.type == EventType.SIGNAL:
                            portfolio.update_signal(event)
                        elif event.type == EventType.ORDER:
                            execution.execute_order(event)
                        elif event.type == EventType.FILL:
                            logger.info(f"Received Fill for {event.symbol} at {event.fill_cost}")
                            # Log to DB
                            db = get_session()
                            trade = TradeRecord(
                                symbol=event.symbol,
                                direction=event.direction,
                                quantity=event.quantity,
                                fill_price=event.fill_cost,
                                commission=event.commission
                            )
                            db.add(trade)
                            db.commit()
                            db.close()

            # Sleep to prevent high CPU usage (1 minute polling)
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("System gracefully stopped by user.")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    run_trading_system()
