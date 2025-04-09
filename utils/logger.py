import logging
import sys
from logging.handlers import RotatingFileHandler
import os

class Logger:
    """
    Logger class for managing consistent logging across the application.
    Automatically detects serverless environments (like Vercel) and adjusts accordingly.
    """
    
    def __init__(self, name, log_level=logging.INFO):
        """
        Initialize the logger with the given name and log level.
        
        Args:
            name (str): Name of the logger.
            log_level (int): Logging level (default: logging.INFO).
        """
        self.name = name
        self.log_level = log_level
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'
        
        # Check if running in a serverless environment
        self.is_serverless = "VERCEL" in os.environ or os.environ.get("ENVIRONMENT") == "production"
        
        # Only create log directory if not in a serverless environment
        if not self.is_serverless:
            self.log_dir = 'logs'
            if not os.path.exists(self.log_dir):
                try:
                    os.makedirs(self.log_dir)
                except Exception as e:
                    # If directory creation fails, just log to console
                    print(f"Warning: Could not create log directory: {e}")
                    self.is_serverless = True
            
            self.log_file = os.path.join(self.log_dir, 'athena.log')
        
    def get_logger(self):
        """
        Configure and return the logger instance.
        
        Returns:
            Logger: Configured logger instance.
        """
        # Create logger
        logger = logging.getLogger(self.name)
        
        # If the logger already has handlers, return it to avoid duplicate handlers
        if logger.handlers:
            return logger
            
        logger.setLevel(self.log_level)
        
        # Create formatter
        formatter = logging.Formatter(self.log_format, self.date_format)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        logger.addHandler(console_handler)
        
        # Create file handler only if not in a serverless environment
        if not self.is_serverless:
            try:
                file_handler = RotatingFileHandler(
                    self.log_file, 
                    maxBytes=10485760,  # 10MB
                    backupCount=3
                )
                file_handler.setFormatter(formatter)
                file_handler.setLevel(self.log_level)
                logger.addHandler(file_handler)
            except Exception as e:
                console_handler.setLevel(logging.WARNING)
                logger.warning(f"Could not setup file logging: {e}")
        else:
            logger.info("Running in serverless environment, file logging disabled")
        
        return logger 