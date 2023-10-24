
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
    monitoring_email = f"Hi, something went wrong trying to send following emails for CAST {failed_list}"

    return monitoring_email
