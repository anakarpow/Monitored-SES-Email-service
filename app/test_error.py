

# tesing bounce, rejection and wrong email adress beahviour
# SES API does NOT return data on failure for these use cases


import json
from datetime import datetime

from adresses import bounce_adress, complaint_adress, wrong_adress_list
from pytest import mark
from utils import send_email_with_attachment, sending_loop

from app import lambda_handler

attachement = '../data/sample_CR.html'


@mark.error
def test_file_no_match():
    """
    tests that projects wothut matchin CR are reported
    file_list values are always correct because extracted from S3 API
    project names might be outdated or wrongly typed
    """
    with open('data/test_file_list.txt', 'r') as file:
        file_list = file.read()
    file_list = file_list.replace('\n', '').split(',')
    file_list = [file.strip() for file in file_list]

    with open('data/test_sending_list_error.json', 'r') as file:
        sending_list = json.load(file)

    for item in sending_list:
        item['timestamp'] = datetime.strptime(item['timestamp'], '%M %Y')
    report = sending_loop(sending_list, file_list)
    assert report['status'] == 0


@mark.error
def test_email_wrong_adress():
    """
    sends to invalid email adresses
    error not caught by SES API
    sender receives warning email 
    """
    for adress in wrong_adress_list:
        resp = send_email_with_attachment(
            target=adress, attachment=attachement)
        print(resp)


@mark.error
def test_bounce():
    """
    sends to testing bounce email adresses > f.e. email rejected by receiver client server
    error not caught by SES API
    sender receives warning email 
    """
    adress = bounce_adress
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)
    print(resp)


@mark.error
def test_complaint():
    """
    sends to testing complaint email adresses > f.e. email added to junk by receiver
    error not caught by SES API
    sender receives warning email 
    """
    adress = complaint_adress
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)
    print(resp)


def test_lambda():
    with open('../events/event_fail.json', 'r') as file:
        event = json.load(file)
    failed = lambda_handler(event, None)
    assert len(failed) > 0
