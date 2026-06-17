from src.core.events import MarketEvent, SignalEvent, EventType
from src.strategy.smc_logic import SMCLogic
from src.utils.logger import logger

class SMCStrategy:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.logic = SMCLogic()

    def calculate_signals(self, event: MarketEvent):
        if event.type != EventType.MARKET:
            return
            
        df = event.data
        if df is None or len(df) < 50:
            return

        df = self.logic.identify_swings(df)
        trend, swing_high, swing_low = self.logic.get_structure(df)
        current_price = df['close'].iloc[-1]
        
        # Use a safe way to get timestamp if 'time' exists in columns
        timestamp = str(df['time'].iloc[-1]) if 'time' in df.columns else "unknown"

        if trend == "NEUTRAL":
            return

        if self.logic.is_in_ote(trend, swing_high, swing_low, current_price):
            logger.info(f"SMCStrategy: {event.symbol} in OTE zone. Trend: {trend}")
            
            signal_type = "LONG" if trend == "BULLISH" else "SHORT"
            sl_price = swing_low if signal_type == "LONG" else swing_high
            
            signal = SignalEvent(
                strategy_id="SMC_V1",
                symbol=event.symbol,
                datetime=timestamp,
                signal_type=signal_type,
                strength=1.0,
                price=current_price,
                sl=sl_price
            )
            self.event_bus.put(signal)
            logger.info(f"SMCStrategy: Generated {signal_type} signal for {event.symbol}")
