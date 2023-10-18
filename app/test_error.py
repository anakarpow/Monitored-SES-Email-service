import json

from adresses import bounce_adress, complaint_adress, wrong_adress_list
from pytest import mark
from utils import send_email_with_attachment

from app import lambda_handler

attachement = '../data/sample_CR.html'


@mark.error
def test_email_wrong_adress():
    for adress in wrong_adress_list:
        resp = send_email_with_attachment(
            target=adress, attachment=attachement)
        print(resp)


@mark.error
def test_bounce():
    adress = bounce_adress
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)
    print(resp)


@mark.error
def test_complaint():
    adress = complaint_adress
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)
    print(resp)


def test_lambda():
    with open('../events/event_fail.json', 'r') as file:
        event = json.load(file)
    failed = lambda_handler(event, None)
    assert len(failed) > 0
