import os
import logging

class LoggerMonitorAgent:
    def __init__(self):
        # Construct the path to the log file relative to this file's directory.
        LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logfiles", "logger_monitor.log")
        # Ensure that the logfiles directory exists.
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        self.logger = logging.getLogger("LoggerMonitorAgent")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers to avoid duplicate logs if this is re-imported.
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # Create a FileHandler to write logs to the log file.
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        # Optionally, create a StreamHandler to also output logs to console.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
    def log_event(self, event: str, details=None):
        """Log an event along with additional details."""
        self.logger.info(f"Event: {event} | Details: {details}")
    
    def log_threat_decision(self, decision_details: dict):
        """Log a threat decision (e.g., response agent outcomes)."""
        self.logger.info(f"Threat Decision: {decision_details}")
