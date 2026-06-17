import pandas as pd
import MetaTrader5 as mt5
from src.core.events import MarketEvent
from src.utils.logger import logger
from src.utils.config import config

class MT5DataHandler:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.symbols = config.symbols
        self.timeframe = config.timeframe_htf

    def _get_mt5_timeframe(self, tf_string: str):
        mapping = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1
        }
        return mapping.get(tf_string.upper(), mt5.TIMEFRAME_H1)

    def update_bars(self):
        for symbol in self.symbols:
            tf = self._get_mt5_timeframe(self.timeframe)
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, 200)
            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                event = MarketEvent(symbol=symbol, data=df)
                self.event_bus.put(event)
            else:
                logger.warning(f"DataHandler: Failed to fetch data for {symbol}")
