import os
from datetime import datetime
from pytz import timezone
import smtplib

import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from config.settings import settings
from utils.bot_files import create_dir


# Provide a class to allow SSL (Not TLS) connection for mail handlers by overloading the emit() method
class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def init_logger():
    # Formatter
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone(settings.time_zone)).timetuple()
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # FileHandler
    log_file_name = os.path.join(settings.logs_dir, settings.log_file)
    create_dir(settings.logs_dir)
    file_handler = TimedRotatingFileHandler(filename=log_file_name,
                                            when='midnight',
                                            backupCount=5)

    # SMTPHandler
    mail_handler = SSLSMTPHandler(mailhost=(settings.smtp, settings.port),
                                  fromaddr=settings.email_from,
                                  toaddrs=settings.email_admin,
                                  subject=settings.logger_name,
                                  credentials=(settings.email_from.split('@')[0], settings.email_pswd),
                                  secure=() if settings.use_tls else None)
    mail_handler.setLevel(logging.WARNING)

    # ConsoleHandler
    console_handler = logging.StreamHandler()

    # BasicConfig
    logging.basicConfig(level=logging.INFO,
                        format=fmtstr,
                        handlers=(file_handler,
                                  console_handler,
                                  mail_handler,
                                  )
                        )
