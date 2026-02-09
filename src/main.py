#!/usr/bin/env python3
"""
API Health Monitor - Main Entry Point
TPM Portfolio Project
"""


import schedule
import time
from datetime import datetime
from .monitor import APIMonitor
from .exporter import GoogleSheetsExporter
from .config import Config

def run_monitoring_cycle():
    """Run a complete monitoring cycle."""
    print(f"\n{'='*60}")
    print(f"API Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Monitor APIs
    monitor = APIMonitor()
    results = monitor.check_all_endpoints()
    
    # Calculate summary statistics
    successful = len([r for r in results if r['status'] == 'healthy'])
    warnings = len([r for r in results if r['status'] == 'warning'])
    errors = len([r for r in results if r['status'] in ['error', 'critical', 'timeout', 'connection_error']])
    
    print(f"\nSummary:")
    print(f"  ✓ Healthy: {successful}/{len(results)}")
    print(f"  ⚠ Warning: {warnings}/{len(results)}")
    print(f"  ✗ Errors:  {errors}/{len(results)}")
    
    # Export to Google Sheets
    if results:
        try:
            exporter = GoogleSheetsExporter()
            exporter.export(results)
        except Exception as e:
            print(f"✗ Export failed: {str(e)}")
    
    return results

def main():
    """Main function with scheduling support."""
    print("🚀 API Health Monitor Starting...")
    print(f"Monitoring {len(Config.get_api_endpoints())} endpoints")
    print(f"Check interval: {Config.get_check_interval()} minutes")
    
    # Run immediately on startup
    run_monitoring_cycle()
    
    # Schedule periodic runs
    schedule.every(Config.get_check_interval()).minutes.do(run_monitoring_cycle)
    
    print(f"\nScheduler started. Press Ctrl+C to exit.\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down API Health Monitor...")

if __name__ == "__main__":
    main()
