import io
import os
import pytz
import requests
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Spacer
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


class ExecutionReport:
    """Holds execution details and can generate reports."""
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.start_time = datetime.now()
        self.duration = None

        self.logo_url = "https://raw.githubusercontent.com/AshanSalinda/EstiMotor/refs/heads/main/Frontend/public/logo.png"
        self.time_zone = "Asia/Colombo"

        self.scraping_errors: list = []
        self.make_model_map: dict = {}
        self.training_metrics: dict = {}


    def add_scraping_errors(self, errors: list):
        print("adding errors:", errors)
        if isinstance(self.scraping_errors, list):
            self.scraping_errors.extend(errors)


    def get_duration(self) -> str:
        """Calculate and return the total duration since start_time."""
        if not self.duration:
            self.duration = str(datetime.now() - self.start_time).split('.')[0]
        return self.duration


    def _build_header(self, title: str):
        """
        Build a branded header with optional logo, title, and generation time.
        """
        elements = []

        # Current timestamp
        now = datetime.now(pytz.timezone(self.time_zone))
        time_text = f"Generated on {now.strftime('%Y-%m-%d %I:%M:%S %p')} ({self.time_zone})"

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

        # Right column: Fetch logo from web
        try:
            response = requests.get(self.logo_url, timeout=10)
            response.raise_for_status()
            logo_data = io.BytesIO(response.content)
            logo = Image(logo_data, width=90, height=36)
        except Exception as e:
            print("Failed to load logo from web:", e)
            logo = Spacer(1, 1)

        # Create table for header layout
        header_table = Table([[left_col, logo]], colWidths=[450, 100])
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


    def generate_scraping_error_report_pdf(self) -> str:
        """
        Generate a PDF report from a list of error dictionaries.
        Each error dict should contain: index, url, error.

        returns the file path of the generated PDF.
        """
        try:
            if not self.scraping_errors or not isinstance(self.scraping_errors, list):
                print("No scraping errors to generate report")
                return ""

            title = "Vehicle Scraping Error Report"
            file_path = os.path.join(self.current_dir, "error_report.pdf")

            doc = SimpleDocTemplate(
                file_path,
                title=title,
                topMargin=20,
                bottomMargin=20,
                pagesize=letter
            )

            elements = self._build_header(title)

            styles = getSampleStyleSheet()
            normal_style = styles["Normal"]

            # -------------------------
            # Table Data
            # -------------------------
            data = [[Paragraph("Index"), Paragraph("URL"), Paragraph("Error")]]

            for err in self.scraping_errors:
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


    def generate_make_model_report_pdf(self) -> str:
        """
        Generate a hierarchical PDF report for the make_model_map with compact spacing and visual level indicators.
        Includes an introductory description to clarify the three-level structure.
        """
        try:
            if not self.make_model_map or not isinstance(self.make_model_map, dict):
                print("No make-model details to generate report")
                return ""

            title = "Make-Model Reference Report"
            file_path = os.path.join(self.current_dir, "make_model_report.pdf")

            doc = SimpleDocTemplate(
                file_path,
                title=title,
                topMargin=20,
                bottomMargin=20,
                pagesize=letter
            )

            elements = self._build_header(title)
            styles = getSampleStyleSheet()

            # -------------------------
            # Intro block (title + legend)
            # -------------------------
            intro_title_style = ParagraphStyle(
                "IntroTitle",
                parent=styles["Heading3"],
                fontName="Helvetica-Bold",
                fontSize=12,
                textColor=colors.HexColor("#062e63"),
                leftIndent=0,
                spaceAfter=6
            )

            intro_sub_style = ParagraphStyle(
                "IntroSub",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                textColor=colors.HexColor("#333333"),
                leading=11,
                leftIndent=0,
                spaceAfter=8
            )

            label_style = ParagraphStyle(
                "Label",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                textColor=colors.HexColor("#062e63"),
                leftIndent=4,
                alignment=0,
            )

            desc_style = ParagraphStyle(
                "Desc",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                textColor=colors.HexColor("#333333"),
                leftIndent=4,
                alignment=0,
                leading=11
            )

            # title row with subtle background
            title_par = Paragraph("About this report", intro_title_style)
            subtitle_par = Paragraph(
                "This document shows vehicle makes and models grouped in three levels: Make → Canonical → Variations.",
                intro_sub_style
            )
            # Put title + subtitle in a single-cell table with background to create a boxed header
            header_table = Table([[title_par], [subtitle_par]], colWidths=[450])
            header_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef6ff")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 6))

            # Legend rows: use a small colored cell on the left (rendered via BACKGROUND) with a Spacer inside
            legend_rows = []
            legend_defs = [
                ("#1a73e8", "> Make", "Manufacturer (top-level)."),
                ("#60a5fa", "* Canonical Model", "Standardized model name representing a group of variations."),
                ("#f7f7f7", "- Variations", "Alternate names or variants replaced by canonical (excluded if same as canonical)."),
            ]
            for color_hex, label, desc in legend_defs:
                # left cell: a tiny square (use Spacer) — background will color it
                left_cell = Spacer(14, 12)
                label_par = Paragraph(label, label_style)
                desc_par = Paragraph(desc, desc_style)
                legend_rows.append([left_cell, label_par, desc_par])

            legend_table = Table(legend_rows, colWidths=[16, 120, 314])
            # style the left column background per row and make the rest clean
            legend_style_cmds: list = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0, colors.transparent),
            ]
            # apply background colors for each left cell
            for i, (color_hex, _, _) in enumerate(legend_defs):
                legend_style_cmds.append(("BACKGROUND", (0, i), (0, i), colors.HexColor(color_hex)))
            legend_table.setStyle(TableStyle(legend_style_cmds))

            elements.append(legend_table)
            elements.append(Spacer(1, 20))

            # -------------------------
            # Styles with shading & hierarchy (compact)
            # -------------------------
            make_style = ParagraphStyle(
                "MakeStyle",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=11,
                textColor=colors.HexColor("#062e63"),
                backColor=colors.HexColor("#e8f0fe"),
                spaceBefore=3,
                spaceAfter=3,
                leftIndent=0,
                borderPadding=3
            )

            canonical_style = ParagraphStyle(
                "CanonicalStyle",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leftIndent=10,
                textColor=colors.HexColor("#1a73e8"),
                backColor=colors.HexColor("#f1f5fb"),
                spaceBefore=1,
                spaceAfter=1,
                borderPadding=2
            )

            variation_style = ParagraphStyle(
                "VariationStyle",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leftIndent=20,
                textColor=colors.HexColor("#111111"),
                backColor=colors.HexColor("#f9f9f9"),  # subtle shading for variations
                spaceBefore=1,
                spaceAfter=1,
                borderPadding=2
            )

            # --------------------------
            # Build content
            # --------------------------
            for make, models in sorted(self.make_model_map.items()):
                # Map canonical -> list of variants
                canonical_map = {}
                for model, canonical in models.items():
                    canonical_map.setdefault(canonical, []).append(model)

                # small count for canonical groups
                canonical_count = f" ({len(canonical_map)})" if len(canonical_map) > 1 else ""
                elements.append(Paragraph(f"> {make}{canonical_count}", make_style))

                for canonical, variants in sorted(canonical_map.items()):
                    variants_count = f" ({len(variants) - 1})" if len(variants) > 1 else ""
                    elements.append(Paragraph(f"* {canonical}{variants_count}", canonical_style))

                    # Variations excluding canonical itself
                    variations_only = [v for v in sorted(variants) if v != canonical]
                    for var in variations_only:
                        elements.append(Paragraph(f"- {var}", variation_style))

                    # tiny space after canonical
                    elements.append(Spacer(1, 2))

                # small space after make block
                elements.append(Spacer(1, 6))

            doc.build(elements)
            print("Generated make-model hierarchy report PDF:", file_path)
            return file_path

        except Exception as e:
            print("Failed to generate make-model report PDF:", e)
            return ""
