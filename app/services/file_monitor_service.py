"""File Monitor Service - Watches homework folder for new submissions"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.services.analysis_service import AnalysisService


class HomeworkFileHandler(FileSystemEventHandler):
    """Handler for new homework files"""
    
    def __init__(self):
        super().__init__()
        self.processed_files = set()
    
    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Check if file has valid extension
        if not self._is_valid_file(file_path):
            return
        
        # Avoid processing the same file multiple times
        if file_path in self.processed_files:
            return
        
        print(f"New homework file detected: {file_path}")
        
        # Wait a moment to ensure file is fully written
        time.sleep(1)
        
        # Process the file based on type
        if file_path.endswith('.json'):
            result = AnalysisService.process_json_submission(file_path)
            if result['success']:
                print(f"Successfully processed: {file_path}")
                print(f"  Submission ID: {result['submission_id']}")
                print(f"  Mistakes found: {result['mistakes']}")
                self.processed_files.add(file_path)
            else:
                print(f"Error processing {file_path}: {result.get('error')}")
        else:
            print(f"Unsupported file type (OCR not yet implemented): {file_path}")
    
    def _is_valid_file(self, file_path):
        """Check if file has valid extension"""
        valid_extensions = ['.json', '.jpg', '.png', '.pdf']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)


class FileMonitorService:
    """Service for monitoring homework submission folder"""
    
    def __init__(self, watch_folder):
        self.watch_folder = watch_folder
        self.observer = None
        self.handler = HomeworkFileHandler()
    
    def start(self):
        """Start monitoring the folder"""
        if not os.path.exists(self.watch_folder):
            os.makedirs(self.watch_folder)
            print(f"Created homework folder: {self.watch_folder}")
        
        self.observer = Observer()
        self.observer.schedule(self.handler, self.watch_folder, recursive=False)
        self.observer.start()
        
        print(f"File monitor started. Watching: {self.watch_folder}")
        print("Supported formats: .json (AI-analyzed), .jpg, .png, .pdf (future OCR)")
    
    def stop(self):
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("File monitor stopped")
    
    def run_forever(self):
        """Run the monitor indefinitely"""
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
