import os

from app.utils.email.email_body import get_completion_email_body
from app.utils.email.email_sender import send_email
from app.utils.execution_report import ExecutionReport


def send_training_completion_email(
    execution_report: ExecutionReport,
) -> None:
    """
    Send a model training completion email with performance metrics and an optional error report.

    Args:
        execution_report : An ExecutionReport object containing all report info.
    """
    recipients=["ashansalinda.as@gmail.com"]
    subject = "Model Training Completed"
    html_body = get_completion_email_body(
        training_duration=execution_report.get_duration(),
        dataset_size=execution_report.dataset_size,
        mae=execution_report.training_metrics.get("MAE") or 'N/A',
        mape=execution_report.training_metrics.get("MAPE") or 'N/A',
        r2_score=execution_report.training_metrics.get("R2") or 'N/A',
        total_errors=len(execution_report.scraping_errors)
    )
    attachments = []

    scraping_error_report_path = execution_report.generate_scraping_error_report_pdf()
    if scraping_error_report_path:
        attachments.append(scraping_error_report_path)

    make_model_report_path = execution_report.generate_make_model_report_pdf()
    if make_model_report_path:
        attachments.append(make_model_report_path)

    send_email(recipients, subject, html_body, attachments)

    os.remove(scraping_error_report_path) if scraping_error_report_path else None
    os.remove(make_model_report_path) if make_model_report_path else None
