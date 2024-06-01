from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP

from config import settings


async def send_mail(subject, msg, files=None):
    message = MIMEMultipart()
    message["From"] = settings.email_from
    message["To"] = settings.email_to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    # if files:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(files) as responce:
    #             buffer = io.BytesIO(await responce.read())
    #             part = MIMEApplication(buffer.read(), Name=url.split('/')[-1])
    #             part['Content-Disposition'] = f'attachment; filename={url.split("/")[-1]}'
    #     message.attach(part)

    smtp_client = SMTP(hostname=settings.smtp, port=settings.port, use_tls=settings.use_tls)
    async with smtp_client:
        await smtp_client.login(settings.email_from, settings.email_pswd)
        await smtp_client.send_message(message)
