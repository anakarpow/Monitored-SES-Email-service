import json

from adresses import adress_list
from pytest import mark
from utils import send_email_with_attachment

from app import lambda_handler

with open('../events/test0.json', 'r') as file:
    event = json.load(file)
    context = {}

attachement = '../data/sample_CR.html'


@mark.basic
def test_email():
    """
    sends email to valid adresses
    asserts SES API received data correctly
    no info on real delivery
    """
    adress = adress_list[0]
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)

    assert 'MessageId' in resp


@mark.skip
@mark.feature
def test_email_list():
    """
    sends multiple emails to valid adresses
    asserts SES API received data correctly
    no info on real delivery
    """
    for adress in adress_list:
        resp = send_email_with_attachment(
            target=adress, attachment=attachement)

    assert 'MessageId' in resp


@mark.skip('find a way to direct to test event from base dir without changing app.py')
@mark.feature
def test_app():
    """
    triggers whole app

    """
    event = '../events/test0_aws.json'
    with open(event, 'r') as file:
        event = json.load(file)
    failed_list = lambda_handler(event, context)
    print(failed_list)
