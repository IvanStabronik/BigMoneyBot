from src.core.events import OrderEvent, FillEvent, EventType
from src.utils.logger import logger
import MetaTrader5 as mt5
from datetime import datetime, timezone

class MT5ExecutionHandler:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def execute_order(self, event: OrderEvent):
        if event.type != EventType.ORDER:
            return

        # Simple execution logic
        logger.info(f"ExecutionHandler: Sending {event.direction} order for {event.symbol} Qty: {event.quantity}")
        
        # Here we would normally use MT5 to place the order
        # Assuming execution succeeds for this architecture design
        
        # Create a FillEvent
        fill = FillEvent(
            timeindex=str(datetime.now(timezone.utc)),
            symbol=event.symbol,
            exchange="MT5",
            quantity=event.quantity,
            direction=event.direction,
            fill_cost=event.sl # Using SL just as a mock fill price for now
        )
        self.event_bus.put(fill)
        logger.info(f"ExecutionHandler: Emitted FillEvent for {event.symbol}")
