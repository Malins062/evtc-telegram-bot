import asyncio
import mimetypes
import os
import tempfile
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from config_data.config import settings
from states.states import Card
from utils.common import get_json_file


async def send_data(bot_id: int, data: Card):
    try:
        files = [get_json_file(data)]
        mail = send_mail(f'{bot_id}', data, files=files)
        await asyncio.gather(asyncio.create_task(mail))
    except Exception:
        return Exception


def get_attachment_tempfile(file: tempfile):
    file_name = file.name
    file_ext = file.name.split('.')[-1]  # extension file
    # attachment = MIMEApplication(file.open('rb').read(), _subtype=file_ext)
    file.seek(0)
    data = file.read()
    attachment = MIMEApplication(data, _subtype=file_ext)
    attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    return attachment


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
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")

            if file_type == "text":
                with open(f"attachments/{file}") as f:
                    file = MIMEText(f.read())
            elif file_type == "image":
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEImage(f.read(), subtype)
            file.add_header('content-disposition', 'attachment', filename=filename)
            message.attach(file)

    smtp_client = SMTP(hostname=settings.smtp, port=settings.port, use_tls=settings.use_tls)
    async with smtp_client:
        await smtp_client.login(settings.email_from, settings.email_pswd)
        await smtp_client.send_message(message)
