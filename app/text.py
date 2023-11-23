
from datetime import datetime


def default_text(variables):
    variables['delta_forecast_limit'] = variables['cost_limit'] - \
        variables['forecast']

    default = f"""
        <html>
        <head></head>
        <body>
        <h1>AWS SES Test {variables['project_name']} </h1>
        <p>Dear Ladies and Gentlemen,</p>
        <p> please find attached the DPP Cost Report for {variables['timestamp']} for the project {variables['project_name']}, including Cloud-Trail costs. </p>

        <p> If the projects AWS consumption follows the trend of the past months, the AWS consumption will be in total ~€ {variables['forecast']} by the end of the year.
        The provided cost limit is € {variables['cost_limit']} - (if no limit was provided “-“ is shown).
        Please note that this leads to a difference of € {variables['delta_forecast_limit']}. <p>

        If you have any questions about the DPP Cost Reports, please feel free to contact us at <a href="dpp.clearing.office.vwag.r.wob@volkswagen.de."> dpp.clearing.office.vwag.r.wob@volkswagen.de </a>

        <p> AWS Consumption can also be tracked via the AWS Cost Review Dashboard. <p>

        General information can be found in the <a href="https://volkswagen-net.de/wikis/display/DigitalProductionPlatform/DPP+Service+Offering">  DPP WIKI</a>.

        <p> Best regards, <p>
        <a>  DPP Clearing Office<a>
        </p>
        </body>
        </html>"""
    return default


def monitoring_text(failed_list):
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    monitoring_email = f"""Hi, attached find the sending report for CAST launched at {timestamp}.\n
    {len(failed_list)} project/s triggered an error.\n
    See the report for more details."""

    return monitoring_email


def rollout_text():
    text = """
        <html>
        <head></head>
        <body>
        <h1>AWS SES Test ROLLOUT </h1>
        <p>Dear Ladies and Gentlemen,</p>
        <p>KEINE PANIK AUF DER TITANIC </p>
        
        <p> Best regards, <p>
        <a>  DPP Clearing Office<a>
        </p>
        </body>
        </html>"""
    return text
