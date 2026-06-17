import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # MT5 Configuration
    mt5_path: str = ""
    mt5_login: int = 0
    mt5_password: str = ""
    mt5_server: str = ""
    
    # Trading Configuration
    symbols: List[str] = ["EURUSD", "XAUUSD"]
    timeframe_htf: str = "H1"
    timeframe_ltf: str = "M5"
    
    # Risk Management
    risk_per_trade_percent: float = 1.0
    reward_ratio: float = 3.0
    max_daily_drawdown: float = 5.0
    
    # DB
    db_url: str = "sqlite:///trades.db"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

config = Settings()
