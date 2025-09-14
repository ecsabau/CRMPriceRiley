import logging
from datetime import datetime
import os

class Logger:
    def __init__(self, name="investor_ai"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if not exists
        os.makedirs("logs", exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(
            f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log(self, message: str, level: str = "info"):
        getattr(self.logger, level.lower())(message)