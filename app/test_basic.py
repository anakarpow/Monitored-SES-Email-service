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
    adress = adress_list[0]
    resp = send_email_with_attachment(
        target=adress, attachment=attachement)

    assert 'MessageId' in resp


@mark.skip
@mark.feature
def test_email_list():
    for adress in adress_list:
        resp = send_email_with_attachment(
            target=adress, attachment=attachement)

    assert 'MessageId' in resp


@mark.feature
def test_app():
    failed_list = lambda_handler(event, context)
    print(failed_list)
