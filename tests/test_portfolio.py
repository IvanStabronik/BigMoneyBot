import pytest
from src.core.events import SignalEvent
from src.core.event_bus import EventBus
from src.portfolio.portfolio import Portfolio
from src.portfolio.risk_manager import RiskManager

def test_risk_manager():
    rm = RiskManager(10000.0) # 100 risk per trade
    qty = rm.calculate_position_size(100.0, 99.0) # 1.0 distance
    assert qty == 100.0

def test_portfolio_signal_handling():
    bus = EventBus()
    portfolio = Portfolio(bus, 10000.0)
    
    # 1.0 distance SL -> $100 risk -> qty 100
    signal = SignalEvent("SMC_1", "EURUSD", "2023", "LONG", 1.0, 100.0, 99.0)
    portfolio.update_signal(signal)
    
    assert bus.empty() == False
    order = bus.get()
    assert order.symbol == "EURUSD"
    assert order.direction == "BUY"
    assert order.quantity == 100.0
    assert order.tp == 103.0 # 3.0 RR
