import openpyxl
import os
from datetime import datetime
from utils import METRICS_FILE

HEADER = [
    'SessionID', 'Timestamp', 'E2E Delay', 'TIFT', 'TTFB', 'Total Latency', 'Usage Summary', 'Conversation Summary'
]

def init_metrics_file():
    """Initialize the metrics Excel file"""
    # Create directory if it doesn't exist
    metrics_dir = os.path.dirname(METRICS_FILE)
    if metrics_dir and not os.path.exists(metrics_dir):
        os.makedirs(metrics_dir)
    
    # Create file if it doesn't exist
    if not os.path.exists(METRICS_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Session Metrics"
        ws.append(HEADER)
        wb.save(METRICS_FILE)
        print(f"Created metrics file: {METRICS_FILE}")

def log_session_metrics(session_id, e2e_delay, tift, ttfb, total_latency, usage_summary, summary):
    """Log session metrics to Excel file"""
    try:
        wb = openpyxl.load_workbook(METRICS_FILE)
        ws = wb.active
        ws.append([
            session_id,
            datetime.now().isoformat(),
            round(e2e_delay, 3),
            round(tift, 3),
            round(ttfb, 3),
            round(total_latency, 3),
            usage_summary,
            summary
        ])
        wb.save(METRICS_FILE)
        print(f"✅ Metrics logged to {METRICS_FILE}")
    except Exception as e:
        print(f"Error logging metrics: {e}")
