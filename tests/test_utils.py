import os
from src.utils.logger import setup_logger
from src.utils.config import Settings

def test_logger():
    logger = setup_logger("TestLogger")
    assert logger.name == "TestLogger"
    assert logger.level == 20 # logging.INFO

def test_config_defaults():
    # Test that defaults are correctly loaded when no env variables are passed
    # Settings will automatically load from .env if present in the current dir.
    # To test raw instantiation without .env overriding with unexpected values, 
    # we use _env_file=None
    settings = Settings(_env_file=None)
    assert settings.risk_per_trade_percent == 1.0
    assert settings.reward_ratio == 3.0
    assert "EURUSD" in settings.symbols
