
from datetime import datetime


def default_text(email_template, variables):
    variables['delta_forecast_limit'] = variables['cost_limit'] - \
        variables['forecast']

    default = f"""
        <html>
        <head></head>
        <body>
        <p>Dear Ladies and Gentlemen,</p>
        <p> please find attached the Cost Report for {variables['timestamp']} for the tenant {variables['project_name']}, including Cloud-Trail costs.   </p>
        <a>
        {email_template}</a>


        <p> The Forecast for 2024 of the Tenant is € {variables['forecast']}.  
        The provided cost limit is € {variables['cost_limit']} - (if no limit was provided “-“ is shown).
        Please note that this leads to a difference of € {variables['delta_forecast_limit']}. <p>
        
        <p> Best regards, <p>
        <a>  Your friendly Office<a>
        </p>
        </body>
        </html>"""
    return default

def monitoring_text(failed_list):
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    monitoring_email = f"""Hi, attached find the sending report launched at {timestamp}.\n
    {len(failed_list)} project/s triggered an error.\n
    See the report for more details."""

    return monitoring_email
