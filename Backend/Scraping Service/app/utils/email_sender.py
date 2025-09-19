import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app.config import settings
from app.utils.templates.email_body import get_completion_email_body
from app.utils.templates.error_report import generate_error_report_pdf


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
        msg["From"] = sender_address
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


def send_training_completion_email(
    training_duration: str,
    total_records: int,
    mae: float,
    mape: float,
    r2_score: float,
    errors: list,
) -> None:
    """
    Send a model training completion email with performance metrics and an optional error report.

    Args:
        training_duration : Duration of the training process as a string (e.g., "00:30:45").
        total_records : Total number of records processed during training.
        mae : Mean Absolute Error of the trained model.
        mape : Mean Absolute Percentage Error of the trained model.
        r2_score : R² Score of the trained model.
        errors : A list of error messages encountered during training. If empty, no error report is attached.
    """
    recipients=["ashansalinda.as@gmail.com"]
    subject = "Model Training Completed"
    html_body = get_completion_email_body(
        training_duration=training_duration,
        total_records=total_records,
        mae=mae,
        mape=mape,
        r2_score=r2_score,
        total_errors=len(errors)
    )
    report_path = generate_error_report_pdf(errors) if errors else ""
    attachments = [report_path] if report_path else []
    send_email(recipients, subject, html_body, attachments)
