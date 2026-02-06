import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any
import os
from .config import Config

class GoogleSheetsExporter:
    """Export monitoring results to Google Sheets."""
    
    def __init__(self):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(
            Config.get_google_creds(),
            self.scope
        )
        self.client = gspread.authorize(self.creds)
        self.sheet_name = Config.get_sheet_name()
    
    def _ensure_headers(self, sheet) -> None:
        """Ensure headers exist in the sheet."""
        headers = [
            'Timestamp (UTC)',
            'API Endpoint',
            'Status',
            'Status Code',
            'Latency (ms)',
            'Error Message'
        ]
        
        # Check if headers exist
        existing_headers = sheet.row_values(1)
        if not existing_headers:
            sheet.append_row(headers)
        elif existing_headers != headers:
            # Update headers if they don't match
            for i, header in enumerate(headers, start=1):
                sheet.update_cell(1, i, header)
    
    def format_results(self, results: List[Dict[str, Any]]) -> List[List[str]]:
        """
        Format results for Google Sheets.
        
        Args:
            results: List of monitoring results
            
        Returns:
            List of rows for Google Sheets
        """
        rows = []
        for result in results:
            rows.append([
                result['timestamp'],
                result['url'],
                result['status'],
                str(result['status_code']) if result['status_code'] else '',
                str(result['latency_ms']) if result['latency_ms'] else '',
                result['error'] if result['error'] else ''
            ])
        return rows
    
    def export(self, results: List[Dict[str, Any]]) -> None:
        """
        Export results to Google Sheets.
        
        Args:
            results: List of monitoring results
        """
        try:
            # Open the sheet
            sheet = self.client.open(self.sheet_name).sheet1
            
            # Ensure headers exist
            self._ensure_headers(sheet)
            
            # Format and append results
            rows = self.format_results(results)
            
            # Append rows in batches of 100 to avoid rate limits
            for i in range(0, len(rows), 100):
                batch = rows[i:i+100]
                sheet.append_rows(batch)
            
            print(f"✓ Successfully exported {len(rows)} rows to Google Sheets")
            print(f"  Sheet: {self.sheet_name}")
            
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"✗ Error: Google Sheet '{self.sheet_name}' not found")
            print(f"  Make sure the sheet exists and is shared with the service account")
        except Exception as e:
            print(f"✗ Error exporting to Google Sheets: {str(e)}")