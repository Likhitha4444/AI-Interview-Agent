import logging
import os
from logging.handlers import RotatingFileHandler
from app.constants import LOG_FOLDER

def setup_logging():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    log_file = os.path.join(LOG_FOLDER, "interview_agent.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3),
            logging.StreamHandler()
        ]
    )

setup_logging()
