from validate_email import validate_email, validate_email_or_fail

adresses = [
    "bou@simulator.amazonses.com", "fabrio.dellagiacoma@outook.com",]


def validate_dpp_email(item):
    print(item)
    r = validate_email_or_fail(
        email_address=item, check_dns=True, dns_timeout=3,
        check_smtp=False)
    print(r)


for item in adresses:
    # validate_dpp_email(item)
    validate_email(item)
