import pandas as pd

class SMCLogic:
    @staticmethod
    def identify_swings(df: pd.DataFrame, length: int = 5) -> pd.DataFrame:
        highs = df['high'].rolling(window=length*2+1, center=True).max()
        lows = df['low'].rolling(window=length*2+1, center=True).min()
        df['swing_high'] = df['high'] == highs
        df['swing_low'] = df['low'] == lows
        return df

    @staticmethod
    def get_structure(df: pd.DataFrame):
        swings_high = df[df['swing_high']]
        swings_low = df[df['swing_low']]
        
        if len(swings_high) < 2 or len(swings_low) < 2:
            return "NEUTRAL", 0.0, 0.0
            
        last_high = swings_high['high'].iloc[-1]
        prev_high = swings_high['high'].iloc[-2]
        
        last_low = swings_low['low'].iloc[-1]
        prev_low = swings_low['low'].iloc[-2]
        
        trend = "NEUTRAL"
        if last_high > prev_high and last_low > prev_low:
            trend = "BULLISH"
        elif last_high < prev_high and last_low < prev_low:
            trend = "BEARISH"
            
        return trend, float(last_high), float(last_low)

    @staticmethod
    def is_in_ote(trend: str, swing_high: float, swing_low: float, current_price: float) -> bool:
        diff = abs(swing_high - swing_low)
        if trend == "BULLISH":
            return (swing_high - diff * 0.786) <= current_price <= (swing_high - diff * 0.618)
        elif trend == "BEARISH":
            return (swing_low + diff * 0.618) <= current_price <= (swing_low + diff * 0.786)
        return False
