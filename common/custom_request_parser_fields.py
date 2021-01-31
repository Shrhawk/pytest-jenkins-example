import datetime

from credit_card_checker import CreditCardChecker
from dateutil.parser import parse


def validate_card_number(value):
    """
    Validate the card number using luhn algorithm
    :param value: str|int
    :return:
    """
    if CreditCardChecker(value).valid():
        return value
    raise ValueError('Invalid card number {card_number}'.format(card_number=value))


def validate_security_code(value):
    if not str(value).isdigit():
        raise ValueError('Invalid security code must be digits')
    if len(value) == 3:
        return value
    raise ValueError('Invalid security code length must be equal to 3')


def validate_date(value):
    """
    Validate date for future
    :param value: str (YYYY-MM-DD) format
    :return: datetimee
    """
    try:
        converted_date = parse(value)
    except Exception:
        raise ValueError('Invalid date must be in the form of YYYY-MM-DD')

    if converted_date < datetime.datetime.now():
        raise ValueError('Invalid date must future date')
    return converted_date


def validate_amount(value):
    """
    Validate Amount must be positive number
    :param value:
    :return:
    """
    try:
        converted_amount = float(value)
    except ValueError:
        raise ValueError('Invalid amount')

    if converted_amount > 0:
        return converted_amount
    raise ValueError('Invalid amount must be positive value')
