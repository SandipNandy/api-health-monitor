import os
import yaml
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()

class Config:
    """Configuration manager for the API health monitor."""
    
    @staticmethod
    def get_api_endpoints() -> List[str]:
        """Get list of API endpoints to monitor."""
        endpoints = os.getenv('API_ENDPOINTS')
        return eval(endpoints)
    
    @staticmethod
    def get_google_creds() -> Dict[str, Any]:
        """Get Google Sheets credentials from environment."""
        import json
        creds_json = os.getenv('GOOGLE_CREDS')
        if not creds_json:
            raise ValueError("GOOGLE_CREDS environment variable not set")
        return json.loads(creds_json)
    
    @staticmethod
    def get_sheet_name() -> str:
        """Get Google Sheet name."""
        return os.getenv('GOOGLE_SHEET_NAME', 'API_Health_Log')
    
    @staticmethod
    def get_thresholds() -> Dict[str, int]:
        """Get latency thresholds in milliseconds."""
        return {
            'warning': int(os.getenv('LATENCY_WARNING', 500)),
            'critical': int(os.getenv('LATENCY_CRITICAL', 1000))
        }
    
    @staticmethod
    def get_check_interval() -> int:
        """Get check interval in minutes."""
        return int(os.getenv('CHECK_INTERVAL', 15))