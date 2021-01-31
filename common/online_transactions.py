from common.constants import (
    DEFAULT_RESPONSE, STATUS_FORCE_LIST, UNAVAILABLE_MESSAGE, UNAVAILABLE_STATUS_CODE, UNPROCESSABLE_ENTITY_CODE,
    UNPROCESSABLE_ENTITY_MESSAGE
)
from common.requests_helper import make_request


class OnlineTransaction(object):
    card_number = None
    card_holder_name = None
    expiration_date = None
    security_code = None
    amount = None
    transaction_class = None
    request_data = {}
    response = {}
    is_expensive_gate_away = False

    def __init__(self, card_number, card_holder_name, expiration_date, amount, security_code=None):
        self.card_number = card_number
        self.card_holder_name = card_holder_name
        self.expiration_date = expiration_date
        self.amount = amount
        self.security_code = security_code
        self.request_data = {
            'card_number': self.card_number,
            'card_holder_name': self.card_holder_name,
            'expiration_date': self.expiration_date,
            'amount': self.amount,
            'security_code': self.security_code
        }

    def make_transaction(self, transaction_class=None):
        """
        Online PaymentGateway flow
        :param transaction_class:
        :return:
        """
        if transaction_class:
            self.transaction_class = transaction_class
        elif 0 < self.amount < 20:
            self.transaction_class = CheapPaymentGateway()
        elif 20 < self.amount < 501:
            self.transaction_class = ExpensivePaymentGateway()
            self.is_expensive_gate_away = True
        elif self.amount > 500:
            self.transaction_class = PremiumPaymentGateway()
        else:
            self.response = {'status_code': UNPROCESSABLE_ENTITY_CODE, 'data': UNPROCESSABLE_ENTITY_MESSAGE}
            return self.response

        if self.transaction_class and self.transaction_class.check_availability():
            self.response = self.transaction_class.make_transaction(data=self.request_data)
            # if the ExpensivePaymentGateway is busy or something went wrong try with
            # CheapPaymentGateway
            if self.is_expensive_gate_away and self.response['status_code'] in STATUS_FORCE_LIST:
                self.is_expensive_gate_away = False
                return self.make_transaction(transaction_class=CheapPaymentGateway())
        else:
            # if the ExpensivePaymentGateway is not available try with CheapPaymentGateway
            if self.is_expensive_gate_away:
                self.is_expensive_gate_away = False
                return self.make_transaction(transaction_class=CheapPaymentGateway())
            else:
                self.response = {'status_code': UNAVAILABLE_STATUS_CODE, 'data': UNAVAILABLE_MESSAGE}
        return self.response


class BasePaymentGateway(object):
    api_key = ''
    api_url = ''
    availability_url = ''
    transaction_url = ''
    response_data = {
        'status_code': 200,
        'data': DEFAULT_RESPONSE
    }
    retries = 0

    def check_availability(self):
        """
        Verify the payment gateway availability
        :return: bool
        """
        response = make_request(api_url=self.availability_url, api_key=self.api_key)
        return response['status_code'] == 200


class CheapPaymentGateway(BasePaymentGateway):
    api_key = '123456789'
    api_url = 'https://cheap-payment-gateway/api/v1'
    availability_url = api_url + '/availability/'
    transaction_url = api_url + '/transaction/'

    def make_transaction(self, data={}):
        """
        Perform CheapPaymentGateway transaction request
        :param data:
        :return:
        """
        response = make_request(
            method='post',
            api_url=self.transaction_url,
            api_key=self.api_key,
            data=data,
            retries=self.retries
        )
        self.response_data['status_code'] = response['status_code']
        self.response_data['data'] = response['data']
        return self.response_data


class ExpensivePaymentGateway(BasePaymentGateway):
    api_key = '987654321'
    api_url = 'https://expensive-payment-gateway/api/v1'
    availability_url = api_url + '/availability/'
    transaction_url = api_url + '/transaction/'

    def make_transaction(self, data={}):
        """
        Perform ExpensivePaymentGateway transaction request
        :param data:
        :return:
        """
        response = make_request(
            method='post',
            api_url=self.transaction_url,
            api_key=self.api_key,
            data=data,
            retries=self.retries
        )
        self.response_data['status_code'] = response['status_code']
        self.response_data['data'] = response['data']
        return self.response_data


class PremiumPaymentGateway(BasePaymentGateway):
    api_key = '123412348'
    api_url = 'https://premium-payment-gateway/api/v1'
    availability_url = api_url + '/availability/'
    transaction_url = api_url + '/transaction/'
    retries = 3

    def make_transaction(self, data={}):
        """
        Perform PremiumPaymentGateway transaction request
        :param data:
        :return:
        """
        response = make_request(
            method='post',
            api_url=self.transaction_url,
            api_key=self.api_key,
            data=data,
            retries=self.retries
        )
        self.response_data['status_code'] = response['status_code']
        self.response_data['data'] = response['data']
        return self.response_data
