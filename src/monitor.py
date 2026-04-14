import requests
import time
from typing import Dict, Any, Tuple
from datetime import datetime
from .config import Config


class APIMonitor:
    """Monitor API health and collect metrics."""
    
    def __init__(self):
        self.thresholds = Config.get_thresholds()
    
    def check_endpoint(self, url: str) -> Dict[str, Any]:
        """
        Check a single API endpoint.
        
        Args:
            url: API endpoint URL
            
        Returns:
            Dictionary containing monitoring results
        """
        result = {
            'url': url,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'unknown',
            'status_code': None,
            'latency_ms': None,
            'error': None
        }
        
        start_time = time.time()
        
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': 'API-Health-Monitor/1.0'}
            )
            
            latency_ms = (time.time() - start_time) * 1000
            result['latency_ms'] = round(latency_ms, 2)
            result['status_code'] = response.status_code
            
            # Determine status based on response
            if response.status_code >= 200 and response.status_code < 300:
                if latency_ms < self.thresholds['warning']:
                    result['status'] = 'healthy'
                elif latency_ms < self.thresholds['critical']:
                    result['status'] = 'warning'
                else:
                    result['status'] = 'critical'
            else:
                result['status'] = 'error'
                
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error'] = 'Request timed out after 10 seconds'
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error'] = 'Connection failed'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def check_all_endpoints(self) -> list:
        """
        Check all configured API endpoints.
        
        Returns:
            List of results for each endpoint
        """
        endpoints = Config.get_api_endpoints()
        results = []
        
        for endpoint in endpoints:
            print(f"Checking {endpoint}...")
            result = self.check_endpoint(endpoint)
            results.append(result)
            
            # Add human-readable summary
            print(f"  Status: {result['status'].upper()}")
            if result['latency_ms']:
                print(f"  Latency: {result['latency_ms']}ms")
            if result['error']:
                print(f"  Error: {result['error']}")
            print()
        
        return results
