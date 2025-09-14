import requests
import re
from typing import Optional

class EmailVerifier:
    def __init__(self, hunter_api_key: str = None):
        self.hunter_api_key = hunter_api_key
        self.free_checks = 50  # Hunter.io free tier limit

    def verify(self, email: str) -> Optional[dict]:
        """Verify email using Hunter.io or regex fallback"""
        if self.hunter_api_key and self.free_checks > 0:
            try:
                response = requests.get(
                    f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.hunter_api_key}",
                    timeout=5
                )
                self.free_checks -= 1
                return {
                    'status': response.json()['data']['status'],
                    'score': response.json()['data']['score']
                }
            except:
                pass
        
        # Fallback regex verification
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'status': 'regex_valid', 'score': 50}
        return {'status': 'invalid', 'score': 0}