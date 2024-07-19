import os
from email.message import EmailMessage
import email.utils
import smtplib

import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from bot.config.settings import settings
from bot.utils.bot_files import create_dir


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

            msg = EmailMessage()
            msg["From"] = self.fromaddr
            msg["To"] = ",".join(self.toaddrs)
            msg["Subject"] = self.getSubject(record)
            msg["Date"] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg, self.fromaddr, self.toaddrs)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as err:
            print(err)
            self.handleError(record)


def init_logger():
    # Formatter
    # logging.Formatter.converter = lambda *args: datetime.now(tz=timezone(settings.time_zone)).timetuple()
    simple_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )

    # FileHandler
    log_file_name = os.path.join(settings.logger.dir, settings.logger.filename)
    create_dir(settings.logger.dir)
    file_handler = TimedRotatingFileHandler(
        filename=log_file_name, when="midnight", backupCount=5
    )
    file_handler.setFormatter(detailed_formatter)

    # SMTPHandler
    mail_handler = SSLSMTPHandler(
        mailhost=(settings.postage.sender_smtp, settings.postage.sender.port),
        fromaddr=settings.postage.sender_email,
        toaddrs=settings.admin.email,
        subject=settings.logger.name,
        credentials=(settings.postage.sender_email.split("@")[0], settings.postage.sender_pswd),
        secure=() if settings.postage.sender_use_tls else None,
    )
    mail_handler.setLevel(logging.WARNING)
    mail_handler.setFormatter(detailed_formatter)

    # ConsoleHandler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)

    # BasicConfig
    logging.basicConfig(
        level=logging.INFO,
        handlers=(
            file_handler,
            console_handler,
            mail_handler,
        ),
    )
