import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from config_data.config import settings


def init_logger():
    # Formatter
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # FileHandler
    root_path = Path(__file__).resolve().parents[1]
    log_file_name = os.path.join(root_path, settings.log_dir, settings.log_file)
    file_handler = TimedRotatingFileHandler(filename=log_file_name,
                                            when='midnight',
                                            backupCount=5)

    # ConsoleHandler
    console_handler = logging.StreamHandler()

    # BasicConfig
    logging.basicConfig(level=logging.INFO,
                        format=fmtstr,
                        handlers=(file_handler, console_handler,))
