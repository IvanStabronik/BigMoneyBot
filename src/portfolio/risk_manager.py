from src.utils.config import config

class RiskManager:
    def __init__(self, account_balance: float):
        self.account_balance = account_balance
        self.risk_per_trade = config.risk_per_trade_percent / 100.0

    def calculate_position_size(self, entry_price: float, sl_price: float) -> float:
        """
        Calculates position size strictly adhering to 1% account risk.
        Simplified for test. In a real scenario, this would use MT5 tick values.
        """
        risk_amount = self.account_balance * self.risk_per_trade
        risk_dist = abs(entry_price - sl_price)
        if risk_dist == 0:
            return 0.0
        
        qty = risk_amount / risk_dist
        return round(qty, 2)
