#!/usr/bin/env python3
"""
MBHB Flask Application Entry Point
Student Performance Analysis and Worksheet Generation System
"""

import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created/verified")
    
    # Run the Flask development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"MBHB Admin Panel Starting")
    print(f"{'='*60}")
    print(f"  URL: http://localhost:{port}")
    print(f"  Debug Mode: {debug}")
    print(f"  Homework Folder: {app.config['HOMEWORK_FOLDER']}")
    print(f"  Worksheet Folder: {app.config['WORKSHEET_FOLDER']}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
