import io
import os
import tempfile
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiogram.client.session import aiohttp
from aiosmtplib import SMTP

from config import settings


def get_attachment_tempfile(file: tempfile):
    file_name = file.name
    file_ext = file.name.split('.')[-1]  # extension file
    # attachment = MIMEApplication(open(file.file.name, 'rb').read(), _subtype=file_ext)
    attachment = MIMEApplication(file.read(), _subtype=file_ext)
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
        if isinstance(files, (list, tuple)):
            for f in files:
                message.attach(get_attachment_tempfile(f))
        else:
            message.attach(get_attachment_tempfile(files))

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(files) as response:
        #         buffer = io.BytesIO(await response.read())
        #         part = MIMEApplication(buffer.read(), Name=files.name)
        #         part['Content-Disposition'] = f'attachment; filename={files.name}'
        #         # part = MIMEApplication(buffer.read(), Name=url.split('/')[-1])
        #         # part['Content-Disposition'] = f'attachment; filename={url.split('/')[-1]}'
        # message.attach(part)

    smtp_client = SMTP(hostname=settings.smtp, port=settings.port, use_tls=settings.use_tls)
    async with smtp_client:
        await smtp_client.login(settings.email_from, settings.email_pswd)
        await smtp_client.send_message(message)
