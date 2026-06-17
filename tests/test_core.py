import pytest
import pandas as pd
from src.core.events import MarketEvent, SignalEvent, OrderEvent, FillEvent, EventType
from src.core.event_bus import EventBus

def test_market_event():
    df = pd.DataFrame({'close': [100.0, 101.0]})
    event = MarketEvent(symbol="EURUSD", data=df)
    assert event.type == EventType.MARKET
    assert event.symbol == "EURUSD"
    assert len(event.data) == 2

def test_signal_event():
    event = SignalEvent("SMC_1", "EURUSD", "2023-01-01", "LONG", 1.0, 1.1000, 1.0900)
    assert event.type == EventType.SIGNAL
    assert event.signal_type == "LONG"
    assert event.sl == 1.0900

def test_order_event():
    event = OrderEvent("EURUSD", "MKT", 1.0, "BUY", 1.0900, 1.1200)
    assert event.type == EventType.ORDER
    assert event.direction == "BUY"
    assert event.quantity == 1.0

def test_fill_event():
    event = FillEvent("2023-01-01", "EURUSD", "MT5", 1.0, "BUY", 1.1000, 0.0)
    assert event.type == EventType.FILL
    assert event.fill_cost == 1.1000

def test_event_bus():
    bus = EventBus()
    assert bus.empty() == True
    
    event = OrderEvent("EURUSD", "MKT", 1.0, "BUY", 1.0900, 1.1200)
    bus.put(event)
    
    assert bus.empty() == False
    
    retrieved_event = bus.get()
    assert retrieved_event.type == EventType.ORDER
    assert bus.empty() == True
