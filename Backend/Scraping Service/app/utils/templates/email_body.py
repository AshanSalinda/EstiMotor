import pytz
from datetime import datetime


def get_completion_email_body(
    training_duration: str,
    total_records: int,
    mae: float,
    mape: float,
    r2_score: float,
    total_errors: int = 0,
    time_zone: str = "Asia/Colombo"
) -> str:
    """
    Returns the HTML body of the completion email.
    The Scraping Error Section is included only if total_errors > 0.
    """

    # Get current date and time in the specified timezone
    now = datetime.now(pytz.timezone(time_zone))
    year_text = str(now.year)
    date_text = now.strftime('%Y-%m-%d')
    time_text = f"{now.strftime('%I:%M:%S %p')} ({time_zone})"

    # Include the error section conditionally
    if total_errors > 0:
        scraping_error_section = f"""
        <div class="error-section">
            <h3>⚠ Scraping Error Report</h3>
            <p>A total of <strong>{total_errors}</strong> errors were detected during vehicle data scraping.
                Please review the attached PDF for a detailed breakdown.</p>
        </div>
            """
    else:
        scraping_error_section = ""

    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Training Completed</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7fb;
            color: #333;
        }}
        .container {{
            width: 100%;
            max-width: 700px;
            margin: 30px auto;
            background-color: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .header {{
            background-color: #062e63;
            color: #ffffff;
            padding: 25px;
            text-align: center;
        }}
        .header img {{
            height: 40px;
            margin-bottom: 10px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .header p {{
            margin: 5px 0 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #1a73e8;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .metrics {{
            margin-top: 40px;
            border-collapse: collapse;
            width: 100%;
            border-radius: 6px;
            overflow: hidden;
        }}
        .metrics th, .metrics td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: center;
            font-size: 14px;
        }}
        .metrics th {{
            background-color: #1a73e8;
            color: #ffffff;
            font-weight: 600;
        }}
        .metrics td {{
            background-color: #f9fbff;
        }}
        .highlight {{
            color: #1a73e8;
            font-weight: bold;
        }}
        .error-section {{
            margin-top: 25px;
            padding: 20px;
            border: 1px solid #f1c0c0;
            background-color: #fff5f5;
            border-radius: 6px;
        }}
        .error-section h3 {{
            margin: 0 0 10px;
            color: #d93025;
            font-size: 18px;
        }}
        .footer {{
            background-color: #062e63;
            padding: 18px 30px;
            color: #b8b8b8;
            font-size: 13px;
            text-align: center;
        }}

        /* Mobile-friendly adjustments */
        @media screen and (max-width: 600px) {{
            .container {{
                width: 95% !important;
                margin: 5px auto !important;
            }}
            .content {{
                padding: 15px !important;
            }}
            .metrics th, .metrics td {{
                font-size: 13px !important;
                padding: 6px !important;
            }}
        }}
    </style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <div class="header">
        <img src="https://raw.githubusercontent.com/AshanSalinda/EstiMotor/refs/heads/main/Frontend/public/logo.png" alt="EstiMotor Logo">
        <h1>EstiMotor Model Training Report</h1>
        <p>Vehicle Price Prediction System</p>
    </div>

    <!-- Content -->
    <div class="content">
        <h2>Model Training Completed ✅</h2>
        <p>Dear Admin,</p>
        <p>The <strong>EstiMotor Vehicle Price Prediction Model</strong> has successfully completed its latest training cycle. Below is a summary of the results:</p>

        <!-- Training Summary -->
        <table class="metrics">
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Training Duration</td>
                <td>{training_duration}</td>
            </tr>
            <tr>
                <td>Total Records Processed</td>
                <td>{total_records}</td>
            </tr>
            <tr>
                <td>Completion Date</td>
                <td>{date_text}</td>
            </tr>
            <tr>
                <td>Completion Time</td>
                <td>{time_text}</td>
            </tr>
            <tr>
                <td>Mean Absolute Error (MAE)</td>
                <td class="highlight">{mae}</td>
            </tr>
            <tr>
                <td>Mean Absolute Percentage Error (MAPE)</td>
                <td class="highlight">{mape}</td>
            </tr>
            <tr>
                <td>R² Score</td>
                <td class="highlight">{r2_score}</td>
            </tr>
        </table>

        <!-- Scraping Error Section -->
        {scraping_error_section}

        <p style="margin-top:25px; font-size:14px; color:#555;">
            This is an automated system notification. If you have concerns about the training job, please check the logs or contact the engineering team.
        </p>
        <p style="font-size:14px; color:#555;">— EstiMotor System</p>
    </div>

    <!-- Footer -->
    <div class="footer">
        &copy; {year_text} EstiMotor. All rights reserved.<br>
        This is an automated email. Please do not reply.
    </div>
</div>
</body>
</html>
    """
