import json
from datetime import datetime

from pytest import mark
from utils_CostReport import send_email_with_attachment

attachement = '../data/sample.html'


with open('events/test_event.json', 'r') as file:
    data = json.load(file)

for item in data['adresses']:
    item['attachment'] = attachement
    item['timestamp'] = datetime.strptime(item['timestamp'], '%M %Y')


@mark.basic
def test_email():
    """
    sends email to valid adresses
    asserts SES API received data correctly
    no info on real delivery
    """
    item = data['adresses'][0]
    resp = send_email_with_attachment(item)

    assert 'MessageId' in resp


@mark.skip
@mark.feature
def test_email_list():
    """
    sends multiple emails to valid adresses
    asserts SES API received data correctly
    no info on real delivery
    """
    adress_list = data['adresses']
    for item in adress_list:
        resp = send_email_with_attachment(item)

    assert 'MessageId' in resp
