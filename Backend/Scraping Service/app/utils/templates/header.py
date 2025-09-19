import os
import pytz
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Image, Spacer, Table, TableStyle


def build_header(title: str, logo_path: str = None, time_zone: str = "Asia/Colombo"):
    """
    Build a branded header with optional logo, title, and generation time.
    """
    elements = []

    # Current timestamp
    now = datetime.now(pytz.timezone(time_zone))
    time_text = f"Generated on {now.strftime('%Y-%m-%d %I:%M:%S %p')} ({time_zone})"

    # -------------------------
    # Styles
    # -------------------------
    title_styles = ParagraphStyle(
        "TitleStyle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=28,
        textColor=colors.HexColor("#555555"),
        alignment=0
    )

    time_styles = ParagraphStyle(
        "TimeStyle",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=10,
        textColor=colors.HexColor("#666666"),
        alignment=0
    )

    # Left column: Title + timestamp
    left_col = [
        Paragraph(title, title_styles),
        Paragraph(time_text, time_styles),
    ]

    # Right column: Logo if exists
    if logo_path and os.path.isfile(logo_path):
        logo_img = Image(logo_path)
        logo_img.drawHeight = 36
        logo_img.drawWidth = 90
    else:
        logo_img = Spacer(1, 1)

    # Create table for header layout
    header_table = Table([[left_col, logo_img]], colWidths=[450, 100])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 4),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 24))
    return elements
