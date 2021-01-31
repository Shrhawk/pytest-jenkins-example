from flask_restful import reqparse

from common.custom_request_parser_fields import (
    validate_amount, validate_card_number, validate_date, validate_security_code
)

request_parser = reqparse.RequestParser(bundle_errors=True)
request_parser.add_argument(
    'CreditCardNumber', type=validate_card_number, required=True, location=['form', 'json']
)
request_parser.add_argument('CardHolder', required=True, type=str, location=['form', 'json'])
request_parser.add_argument('ExpirationDate', required=True, type=validate_date, location=['form', 'json'])
request_parser.add_argument('SecurityCode', type=validate_security_code, location=['form', 'json'])
request_parser.add_argument('Amount', required=True, type=validate_amount, location=['form', 'json'])
