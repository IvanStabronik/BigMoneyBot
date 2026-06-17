import pytest
import pandas as pd
from src.strategy.smc_logic import SMCLogic
from src.strategy.smc_strategy import SMCStrategy
from src.core.events import MarketEvent
from src.core.event_bus import EventBus

def test_smc_logic():
    data = {
        'high': [10, 15, 12, 20, 18],
        'low': [5, 8, 6, 12, 10],
    }
    df = pd.DataFrame(data)
    df = SMCLogic.identify_swings(df, length=1)
    assert 'swing_high' in df.columns
    assert 'swing_low' in df.columns

def test_smc_strategy():
    bus = EventBus()
    strategy = SMCStrategy(bus)
    
    df = pd.DataFrame()
    event = MarketEvent("EURUSD", df)
    strategy.calculate_signals(event)
    
    assert bus.empty() == True
