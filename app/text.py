
from datetime import datetime


def default_text(variables):
    variables['delta_forecast_limit'] = variables['cost_limit'] - \
        variables['forecast']

    default = f"""
        <html>
        <head></head>
        <body>
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


def rollout_text(project_name):
    text = f"""
<html>
<body>
    <p>
        Dear Ladies and Gentlemen, <br>
        We are excited to announce an improvement to our CAST-Service. <br>
    </p>
    <p>
        Starting from today, we will send the Cost Reports using the  <b>AWS-native SES Service</b>.
    </p>
    <p>
        Please confirm that this E-Mail has reached you. <u> A simple empty email is enough.</u> <br>
        In case the email landed in your <u> junk folder</u>, please add ‘junk’ to your answer.
    </p>

    <p>
        <b>Your answer helps us improve our service and therefore your future satisfaction</b>.
    </p>
    <p>
        Also, if this email finds you and you are not the appropriate contact person for the project <u> {project_name}</u>, please update the contact data
        within <a href="https://firestarter.bp.vwgroup.cloud/"> Firestarter </a> under “Billing contact“.
    </p>
    <p>
        Thanks for your cooperation.
    </p>
    <p>
        Best regards,<br>
        DPP Clearing Office
    </p>
</body>
</html>"""
    return text
