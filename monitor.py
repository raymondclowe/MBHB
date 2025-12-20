#!/usr/bin/env python3
"""
File Monitor - Watches homework folder and processes submissions automatically
Run this in a separate process from the Flask app
"""

import os
import sys
from app import create_app
from app.services.file_monitor_service import FileMonitorService

def main():
    """Start the file monitor"""
    app = create_app()
    
    with app.app_context():
        homework_folder = app.config['HOMEWORK_FOLDER']
        
        print(f"\n{'='*60}")
        print(f"MBHB File Monitor Starting")
        print(f"{'='*60}")
        print(f"  Watching: {homework_folder}")
        print(f"  Supported: .json, .jpg, .png, .pdf")
        print(f"  Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        monitor = FileMonitorService(homework_folder)
        monitor.run_forever()

if __name__ == '__main__':
    main()
