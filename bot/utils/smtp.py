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

from bot.config.settings import settings
from bot.states.card_states import Card
from bot.utils.bot_files import create_json_data_file, get_prefix_file_name


def get_html_content(data) -> str:
    try:
        html_template = Template(
            Path(settings.attachment.template_card_answer).read_text(encoding="utf-8")
        )
        content = html_template.substitute(data)
        return content
    except Exception as err:
        return str(err)


async def send_data(subject: str, data: Card):
    try:
        files = (
            {
                "full_filename": create_json_data_file(data),
                "type": "text/json",
                "filename": get_prefix_file_name(data) + settings.attachment.filename_data,
            },
            {
                "full_filename": os.path.join(
                    settings.attachment.dir,
                    f'{data.get("user_id")}-{settings.attachment.filename_protocol}',
                ),
                "type": "image/jpg",
                "filename": data.get("photo_protocol"),
            },
            {
                "full_filename": os.path.join(
                    settings.attachment.dir,
                    f'{data.get("user_id")}-{settings.attachment.filename_tc}',
                ),
                "type": "image/jpg",
                "filename": data.get("photo_tc"),
            },
        )

        mail = send_mail(subject, data, files=files)
        await asyncio.gather(asyncio.create_task(mail))
    except Exception as err:
        return err


async def send_mail(subject, data, files=None):
    if files is None:
        files = []

    message = MIMEMultipart("related")
    message["From"] = settings.postage.sender_email
    message["To"] = settings.postage.recipient_email
    message["Subject"] = subject

    # Add message text HTML
    html_content = get_html_content(data)
    body = MIMEText(html_content, "html", "utf-8")
    message.attach(body)

    # Add files attachments
    if files:
        for file in files:
            temp_filename = file.get("full_filename")
            filename = file.get("filename")
            ftype = file.get("type")
            file_type, subtype = ftype.split("/")

            if file_type == "text":
                with open(temp_filename) as f:
                    file = MIMEText(f.read(), subtype, "utf-8")
            elif file_type == "image":
                with open(temp_filename, "rb") as f:
                    file = MIMEImage(f.read(), subtype)
                file.add_header("Content-ID", f"<{filename}>")
            else:
                with open(temp_filename, "rb") as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header("Content-disposition", "attachment", filename=filename)
            message.attach(file)

    smtp_client = SMTP(
        hostname=settings.postage.sender_smtp, port=settings.postage.sender_port, use_tls=settings.postage.sender_use_tls
    )
    async with smtp_client:
        await smtp_client.login(settings.postage.sender_email, settings.postage.sender_pswd)
        await smtp_client.send_message(message)

    # print('Message sent')
