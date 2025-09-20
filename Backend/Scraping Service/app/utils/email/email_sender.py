import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from app.config import settings


def send_email(recipients: list, subject: str, body: str, attachments: list[str] = None) -> None:
    """
    Send an email with optional attachments to one or more recipients.

    The email can contain either plain text or HTML content. If the `body` starts with
    "<", it will be automatically treated as HTML; otherwise, it is sent as plain text.
    Multiple files of any type (PDFs, images, CSVs, etc.) can be attached.

    Args:
        recipients : A list of recipient email addresses as strings.
        subject : The subject line of the email.
        body : The main content of the email. HTML content is automatically detected if it starts with "<".
        attachments : A list of file paths to attach to the email. Files that do not exist will be skipped.
    """
    try:
        if not recipients:
            raise ValueError("At least one recipient email address must be provided.")
        if not subject:
            raise ValueError("Email subject cannot be empty.")
        if not body:
            raise ValueError("Email body cannot be empty.")

        # Email server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        sender_address = settings.EMAIL_SENDER_ADDRESS
        sender_password = settings.EMAIL_SENDER_PASSWORD


        # Build email
        msg = MIMEMultipart()
        msg["From"] = formataddr(("EstiMotor", sender_address))
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if body.strip().startswith("<") else "plain"))

        # Attach files
        if attachments:
            for file_path in attachments:
                path = Path(file_path)
                if not path.is_file():
                    print(f"Attachment {file_path} not found, skipping.")
                    continue

                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=path.name)
                    # Inform email client that this is an attachment
                    part['Content-Disposition'] = f'attachment; filename="{path.name}"'
                    msg.attach(part)

        # Send email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_address, sender_password)
            server.sendmail(sender_address, recipients, msg.as_string())

        print("Email sent!")

    except Exception as e:
        print("Failed to send email:")
        print(e)
        raise e
