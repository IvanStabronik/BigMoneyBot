from src.core.events import SignalEvent, OrderEvent, EventType
from src.portfolio.risk_manager import RiskManager
from src.utils.logger import logger
from src.utils.config import config

class Portfolio:
    def __init__(self, event_bus, initial_balance=10000.0):
        self.event_bus = event_bus
        self.balance = initial_balance
        self.risk_manager = RiskManager(self.balance)
        self.current_positions = {}

    def update_signal(self, event: SignalEvent):
        if event.type != EventType.SIGNAL:
            return

        if event.symbol in self.current_positions:
            logger.info(f"Portfolio: Already holding position for {event.symbol}. Ignoring signal.")
            return

        qty = self.risk_manager.calculate_position_size(event.price, event.sl)
        
        if qty <= 0:
            logger.warning(f"Portfolio: Calculated qty <= 0 for {event.symbol}. Ignoring.")
            return

        direction = "BUY" if event.signal_type == "LONG" else "SELL"
        
        # Calculate TP based on RR
        risk_dist = abs(event.price - event.sl)
        if direction == "BUY":
            tp = event.price + (risk_dist * config.reward_ratio)
        else:
            tp = event.price - (risk_dist * config.reward_ratio)

        order = OrderEvent(
            symbol=event.symbol,
            order_type="MKT",
            quantity=qty,
            direction=direction,
            sl=event.sl,
            tp=tp
        )
        
        self.event_bus.put(order)
        logger.info(f"Portfolio: Created {direction} OrderEvent for {event.symbol}, Qty: {qty}")
