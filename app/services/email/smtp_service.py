import logging
import aiosmtplib
from email.message import EmailMessage
from config.config import EMAIL_SETTINGS

logger = logging.getLogger(__name__)


class EmailSmtpService:
    def __init__(self):
        self.smtp_server = EMAIL_SETTINGS.SMTP_SERVER
        self.smtp_port = EMAIL_SETTINGS.SMTP_PORT
        self.smtp_username = EMAIL_SETTINGS.SMTP_USERNAME
        self.smtp_password = EMAIL_SETTINGS.SMTP_PASSWORD

    async def send_email(
        self, sender: str, to_email: str, subject: str, body: str, is_html: bool = False
    ):
        try:
            message = EmailMessage()
            message["From"] = sender
            message["To"] = to_email
            message["Subject"] = subject

            if is_html:
                message.add_alternative(body, subtype="html")

            # Для порта 465 используем SSL/TLS
            async with aiosmtplib.SMTP(
                hostname=self.smtp_server,
                port=self.smtp_port,
                use_tls=True,  # Используем TLS для порта 465
            ) as smtp:
                await smtp.connect()
                await smtp.login(self.smtp_username, self.smtp_password)
                await smtp.send_message(message)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
