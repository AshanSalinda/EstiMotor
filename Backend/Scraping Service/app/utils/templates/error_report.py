import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from app.utils.templates.header import build_header


# -------------------------
# PDF generation
# -------------------------
def generate_error_report_pdf(errors: list[dict]) -> str:
    """
    Generate a PDF report from a list of error dictionaries.
    Each error dict should contain: index, url, error.

    returns the file path of the generated PDF.
    """
    try:
        title = "Vehicle Scraping Error Report"

        # Build paths relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "logo.png")
        file_path = os.path.join(current_dir, "error_report.pdf")

        doc = SimpleDocTemplate(
            file_path,
            title=title,
            topMargin=20,
            bottomMargin=20,
            pagesize=letter
        )

        elements = build_header(title=title, logo_path=logo_path)

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]

        # -------------------------
        # Table Data
        # -------------------------
        data = [[Paragraph("Index"), Paragraph("URL"), Paragraph("Error")]]

        for err in errors:
            raw_url = err.get("url")
            url = f'<a target="_blank" href="{raw_url}">{raw_url}</a>' if raw_url else "N/A"
            data.append([
                Paragraph(str(err.get("index", "")), normal_style),
                Paragraph(url, normal_style),
                Paragraph(str(err.get("error", "")), normal_style)
            ])

        # -------------------------
        # Table Styling
        # -------------------------
        table = Table(data, colWidths=[100, 350, 100])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#257fda")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            # All cells
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Non-header rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#dddddd"))
        ]))

        elements.append(table)
        doc.build(elements)

        print("Generated error report PDF:", file_path)
        return file_path

    except Exception as e:
        print("Failed to generate error report PDF:", e)
        return ""
