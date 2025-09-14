import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()  # Load environment variables from .env file

class Config:
    """
    Centralized configuration manager for API keys, rate limits, and timeouts.
    """
    
    # API Keys (loaded from .env)
    MAILJET_API_KEY: str = os.getenv("MAILJET_API_KEY", "")
    MAILJET_SECRET_KEY: str = os.getenv("MAILJET_SECRET_KEY", "")
    HUNTER_API_KEY: str = os.getenv("HUNTER_API_KEY", "")
    
    # Rate Limits (requests per minute)
    RATE_LIMITS: Dict[str, int] = {
        "mailjet": 200,     # Mailjet API limit
        "hunter": 50,       # Hunter.io API limit
        "scraper": 30       # Web scraping limit
    }
    
    # Timeouts (seconds)
    TIMEOUTS: Dict[str, int] = {
        "api_request": 10,
        "database_query": 5,
        "email_send": 15
    }
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get any config value with fallback.
        
        Example:
            Config.get("MAILJET_API_KEY")
            Config.get("RATE_LIMITS.mailjet", 100)
        """
        try:
            if "." in key:
                section, subkey = key.split(".")
                return getattr(Config, section.upper())[subkey.lower()]
            return getattr(Config, key.upper())
        except (AttributeError, KeyError):
            return default