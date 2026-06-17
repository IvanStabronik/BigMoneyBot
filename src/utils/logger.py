import logging
import sys

def setup_logger(name: str = "BigMoneyBot", level: int = logging.INFO) -> logging.Logger:
    """
    Setup a structured logger with console output.
    """
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
