from src.core.events import OrderEvent
from src.core.event_bus import EventBus
from src.execution.mt5_execution import MT5ExecutionHandler

def test_execution_handler():
    bus = EventBus()
    handler = MT5ExecutionHandler(bus)
    
    order = OrderEvent("EURUSD", "MKT", 1.0, "BUY", 1.0900, 1.1200)
    handler.execute_order(order)
    
    assert bus.empty() == False
    fill = bus.get()
    assert fill.type.name == "FILL"
    assert fill.symbol == "EURUSD"
