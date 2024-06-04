import asyncio
import mimetypes
import os
import tempfile
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from config_data.config import settings
from states.states import Card
from utils.common import get_json_file


async def send_data(bot_id: int, data: Card):
    try:
        files = [{
            'temp_filename': get_json_file(data),
            'type': 'text/json',
            'filename': settings.data_file,
        }]
        mail = send_mail(f'{bot_id}', data, files=files)
        await asyncio.gather(asyncio.create_task(mail))
    except Exception as err:
        return err


async def send_mail(subject, msg, files=None):
    if files is None:
        files = []

    message = MIMEMultipart()
    message['From'] = settings.email_from
    message['To'] = settings.email_to
    message['Subject'] = subject
    body = MIMEText(f'<html><body>{msg}</body></html>', 'html', 'utf-8')
    message.attach(body)

    if files:
        for file in files:
            temp_filename = file.get('temp_filename')
            filename = file.get('filename')
            ftype = file.get('type')
            file_type, subtype = ftype.split("/")

            if file_type == "text":
                with open(temp_filename) as f:
                    file = MIMEText(f.read(), subtype)
            elif file_type == "image":
                with open(temp_filename, "rb") as f:
                    file = MIMEImage(f.read(), subtype)
            else:
                with open(temp_filename, "rb") as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            message.attach(file)

    smtp_client = SMTP(hostname=settings.smtp, port=settings.port, use_tls=settings.use_tls)
    async with smtp_client:
        await smtp_client.login(settings.email_from, settings.email_pswd)
        await smtp_client.send_message(message)
