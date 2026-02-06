#!/usr/bin/env python3
"""
CLI Interface for API Health Monitor
"""

import argparse
import sys
from .main import run_monitoring_cycle

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='API Health Monitoring System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run     # Run monitoring once
  %(prog)s daemon  # Run as daemon with scheduling
        """
    )
    
    parser.add_argument(
        'command',
        choices=['run', 'daemon'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def main():
    """CLI entry point."""
    args = parse_args()
    
    if args.command == 'run':
        run_monitoring_cycle()
    elif args.command == 'daemon':
        from .main import main as daemon_main
        daemon_main()

if __name__ == "__main__":
    main()