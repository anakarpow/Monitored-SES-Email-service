import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from adresses import sender
from botocore.exceptions import ClientError
from text import default

ses_client = boto3.client("ses", region_name="eu-west-1")


def send_email_with_attachment(target, attachment):
    """
    supports attachments but no fine tuning in multiple recipients
    accoridng to testing : all adresses are set as Bcc
    """

    # sendig coordinates
    SENDER = sender
    RECIPIENT = target
    bcc_emails = 'cast.ses.1@efs.at'
    ccc_emails = 'cast.ses.1@efs.at'
    msg = MIMEMultipart()
    msg["Subject"] = "This is an email with an attachment!"
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg['Bcc'] = bcc_emails
    msg['Ccc'] = ccc_emails

    # text variables

    # project_name = project_dict['Projekt_Name_neu'][0]
    # timestamp = project_dict['creation_date']
    # forecast = '#NOT_AVAILABLE_YET#'
    # cost_limit = '#NOT_AVAILABLE_YET#'
    # delta_forecast_limit = '#NOT_AVAILABLE_YET#'

    # in the future import text from S3
    # Set message body, adding variables.
    email_text = default

    body = MIMEText(email_text, "html")
    msg.attach(body)

    # In same directory as script
    with open(attachment, "rb") as attachment_data:
        part = MIMEApplication(attachment_data.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=attachment.replace('/tmp/', ''))
    msg.attach(part)

    try:
        # Convert message to string and send
        response = ses_client.send_raw_email(
            Source=SENDER,
            Destinations=[msg['To'], msg['Bcc'], msg['Ccc']],
            RawMessage={"Data": msg.as_string()}
        )
        print("Email sent! Message ID:"),
        return response

    # Display an error if something goes wrong.
    except ClientError as e:
        print(response)
        print(e.response['Error']['Message'])


# if __name__ == "__main__":
#     filename = '../output/2023-06-DPP-AUDI AG-AUDINECKARSULMDATALAKE.html'

#     with open('../test_data/main_dict_5_2022.json', 'r') as file:
#         data = json.load(file)
#         for project, values in data.items():
#             send_email_with_attachment(data[project], filename)
#             exit()
