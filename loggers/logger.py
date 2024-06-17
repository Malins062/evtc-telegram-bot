import os
import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from config_data.config import settings
from utils.bot_files import create_dir


def init_logger():
    # Formatter
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # FileHandler
    log_file_name = os.path.join(settings.logs_dir, settings.log_file)
    create_dir(settings.logs_dir)
    file_handler = TimedRotatingFileHandler(filename=log_file_name,
                                            when='midnight',
                                            backupCount=5)

    # SMTPHandler
    mail_handler = SMTPHandler(mailhost=(settings.smtp, settings.port),
                               fromaddr=settings.email_from,
                               toaddrs=settings.email_admin,
                               subject=settings.logger_name,
                               credentials=(settings.email_from.split('@')[0], settings.email_pswd),
                               secure=() if settings.use_tls else None,
                               timeout=1.0)
    mail_handler.setLevel(logging.WARNING)

    # ConsoleHandler
    console_handler = logging.StreamHandler()

    # BasicConfig
    logging.basicConfig(level=logging.INFO,
                        format=fmtstr,
                        handlers=(file_handler,
                                  console_handler,
                                  # mail_handler,
                                  )
                        )
