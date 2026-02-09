#!/usr/bin/env python3
"""
API Health Monitor - ALL IN ONE FILE
No import issues!
"""


import requests
import time
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 50)
print("🚀 API HEALTH MONITOR - SIMPLE VERSION")
print("=" * 50)

# ================= CONFIGURATION =================
def get_config():
    """Get configuration from .env file."""
    # APIs to monitor
    endpoints_json = os.getenv('API_ENDPOINTS', '["https://httpbin.org/status/200"]')
    endpoints = json.loads(endpoints_json)
    
    # Google credentials
    creds_json = os.getenv('GOOGLE_CREDS')
    if not creds_json:
        print("❌ ERROR: GOOGLE_CREDS not found in .env file")
        print("   Make sure you have GOOGLE_CREDS='{...}' in .env")
        exit(1)
    
    creds = json.loads(creds_json)
    sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'API_Health_Log')
    
    return endpoints, creds, sheet_name

# ================= MONITORING =================
def check_api(url):
    """Check if an API is healthy."""
    print(f"\n🔍 Checking: {url}")
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'latency_ms': None,
        'error': None
    }
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        result['latency_ms'] = round(latency, 2)
        result['status_code'] = response.status_code
        
        if response.status_code == 200:
            if latency < 500:
                result['status'] = 'healthy'
            elif latency < 1000:
                result['status'] = 'warning'
            else:
                result['status'] = 'critical'
        else:
            result['status'] = 'error'
            
        print(f"   ✅ Status: {result['status'].upper()}")
        print(f"   ⏱️  Latency: {result['latency_ms']}ms")
        
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = 'Request timed out'
        print(f"   ❌ Timeout after 10 seconds")
    except requests.exceptions.ConnectionError:
        result['status'] = 'connection_error'
        result['error'] = 'Cannot connect to API'
        print(f"   ❌ Connection failed")
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        print(f"   ❌ Error: {e}")
    
    return result

# ================= GOOGLE SHEETS =================
def save_to_google_sheets(results, creds_dict, sheet_name):
    """Save results to Google Sheets."""
    print(f"\n💾 Saving to Google Sheets: {sheet_name}")
    
    try:
        # 1. Authenticate with Google
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, scope
        )
        client = gspread.authorize(credentials)
        
        # 2. Open the sheet
        sheet = client.open(sheet_name).sheet1
        
        # 3. Add headers if empty
        if not sheet.get_all_values():
            headers = ['Timestamp', 'URL', 'Status', 'Code', 'Latency (ms)', 'Error']
            sheet.append_row(headers)
            print("   Added headers to sheet")
        
        # 4. Add data
        for result in results:
            row = [
                result['timestamp'],
                result['url'],
                result['status'],
                str(result['status_code'] or ''),
                str(result['latency_ms'] or ''),
                result['error'] or ''
            ]
            sheet.append_row(row)
        
        print(f"   ✅ Saved {len(results)} records successfully!")
        return True
        
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"   ❌ ERROR: Sheet '{sheet_name}' not found!")
        print("      Make sure:")
        print("      1. Sheet exists")
        print("      2. Shared with service account")
        print(f"      3. Service account: {creds_dict.get('client_email', 'unknown')}")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {type(e).__name__}: {str(e)}")
        return False

# ================= MAIN FUNCTION =================
def main():
    """Main function."""
    # Get configuration
    endpoints, creds, sheet_name = get_config()
    
    print(f"📊 Monitoring {len(endpoints)} APIs")
    print(f"📁 Saving to: {sheet_name}")
    
    # Check each API
    results = []
    for endpoint in endpoints:
        result = check_api(endpoint)
        results.append(result)
    
    # Save to Google Sheets
    success = save_to_google_sheets(results, creds, sheet_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 FINAL SUMMARY")
    print("=" * 50)
    
    healthy = sum(1 for r in results if r['status'] == 'healthy')
    warning = sum(1 for r in results if r['status'] == 'warning')
    errors = sum(1 for r in results if r['status'] in ['error', 'critical', 'timeout', 'connection_error'])
    
    print(f"✅ Healthy: {healthy}")
    print(f"⚠️  Warning: {warning}")
    print(f"❌ Errors: {errors}")
    print(f"💾 Saved to Sheets: {'Yes' if success else 'No'}")
    
    if success:
        print("\n🎉 SUCCESS! Check your Google Sheet for data.")
    else:
        print("\n😞 Some issues occurred. Check errors above.")

if __name__ == "__main__":
    main()
