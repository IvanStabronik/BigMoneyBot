import pandas as pd
from enum import Enum

class EventType(Enum):
    MARKET = "MARKET"
    SIGNAL = "SIGNAL"
    ORDER = "ORDER"
    FILL = "FILL"

class Event:
    """Base class for all events."""
    pass

class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.type = EventType.MARKET
        self.symbol = symbol
        self.data = data

class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    """
    def __init__(self, strategy_id: str, symbol: str, datetime: str, signal_type: str, strength: float, price: float, sl: float):
        self.type = EventType.SIGNAL
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type  # 'LONG' or 'SHORT'
        self.strength = strength
        self.price = price
        self.sl = sl

class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    """
    def __init__(self, symbol: str, order_type: str, quantity: float, direction: str, sl: float, tp: float):
        self.type = EventType.ORDER
        self.symbol = symbol
        self.order_type = order_type # 'MKT' or 'LMT'
        self.quantity = quantity
        self.direction = direction # 'BUY' or 'SELL'
        self.sl = sl
        self.tp = tp

    def print_order(self):
        print(f"Order: Symbol={self.symbol}, Type={self.order_type}, Quantity={self.quantity}, Direction={self.direction}")

class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage.
    """
    def __init__(self, timeindex: str, symbol: str, exchange: str, quantity: float, direction: str, fill_cost: float, commission: float = 0.0):
        self.type = EventType.FILL
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission
