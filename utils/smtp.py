import asyncio
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from string import Template

from aiosmtplib import SMTP

from config_data.config import settings
from states.states import Card
from utils.common import get_json_file


def get_html_content(data) -> str:
    try:
        html_template = Template(Path('templates/send_card_answer.html').read_text(encoding='utf-8'))
        content = html_template.substitute(data)
        return content
    except Exception as err:
        return str(err)


async def send_data(bot_id: int, data: Card):
    try:
        files = [
            {
                'full_filename': get_json_file(data),
                'type': 'text/json',
                'filename': settings.data_file,
            },
            {
                'full_filename': os.path.join(settings.attachments_dir, data.get('photo_protocol')),
                'type': 'image/jpg',
                'filename': settings.protocol_file,
            },
            {
                'full_filename': os.path.join(settings.attachments_dir, data.get('photo_protocol')),
                'type': 'image/jpg',
                'filename': settings.tc_file,
            },
        ]

        mail = send_mail(f'{bot_id}', data, files=files)
        await asyncio.gather(asyncio.create_task(mail))
    except Exception as err:
        return err


async def send_mail(subject, data, files=None):
    if files is None:
        files = []

    message = MIMEMultipart()
    message['From'] = settings.email_from
    message['To'] = settings.email_to
    message['Subject'] = subject

    # Add files attachments
    if files:
        for file in files:
            temp_filename = file.get('full_filename')
            filename = file.get('filename')
            ftype = file.get('type')
            file_type, subtype = ftype.split('/')

            if file_type == 'text':
                with open(temp_filename) as f:
                    file = MIMEText(f.read(), subtype, 'utf-8')
            elif file_type == 'image':
                with open(temp_filename, 'rb') as f:
                    file = MIMEImage(f.read(), subtype)
            else:
                with open(temp_filename, 'rb') as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            message.attach(file)

    # Add message text HTML
    html_content = get_html_content(data)
    body = MIMEText(html_content, 'html', 'utf-8')
    message.attach(body)

    smtp_client = SMTP(hostname=settings.smtp, port=settings.port, use_tls=settings.use_tls)
    async with smtp_client:
        await smtp_client.login(settings.email_from, settings.email_pswd)
        await smtp_client.send_message(message)
