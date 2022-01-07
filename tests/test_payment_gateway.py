import datetime
from random import choice
from unittest.mock import patch

from common.online_transactions import OnlineTransaction


class TestPaymentGateWay(object):
    """
    Tests for Payment-GateWays
    """

    def test_cheap_payment_gateway(self, app_):
        """
        Test cheap payment gateway response.
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                12,
                security_code=321
            )
            result = transaction_flow.make_transaction()
            # assert result['status_code'] == 201
            status_code = choice([201, 202, 203, 200])
            assert result['status_code'] == status_code
            assert result['data'] == 'ok'

    @patch('common.online_transactions.CheapPaymentGateway.make_transaction')
    def test_cheap_payment_gateway_using_function_calling(self, make_transaction, app_):
        """
        Test cheap payment gateway called with their own class make_transaction function
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                12,
                security_code=321
            )
            transaction_flow.make_transaction()
            make_transaction.assert_called_once()

    def test_premium_payment_gateway(self, app_):
        """
        Test premium payment gateway response.
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                521,  # premium amount
                security_code=321
            )
            result = transaction_flow.make_transaction()
            assert result['status_code'] == 200
            assert result['data'] == 'ok'

    @patch('common.online_transactions.PremiumPaymentGateway.make_transaction')
    def test_premium_payment_gateway_using_function_calling(self, make_transaction, app_):
        """
        Test premium payment gateway called with their own class make_transaction function
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                521,  # premium amount
                security_code=321
            )
            transaction_flow.make_transaction()
            make_transaction.assert_called_once()

    @patch('common.online_transactions.make_request', side_effect=[
        {'data': 'ok', 'status_code': 200}, {'data': 'ok', 'status_code': 200}
    ])
    def test_premium_payment_gateway_retries(self, make_request, app_):
        """
        Test premium payment gateway with retries
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                521,  # premium amount
                security_code=321
            )
            transaction_flow.make_transaction()
            #  second call with transaction call contains retries
            args, kwargs = make_request.call_args_list[1]
            assert kwargs['retries'] == 3

    def test_expensive_payment_gateway(self, app_):
        """
        Test expensive payment gateway response.
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                450,  # expensive amount
                security_code=321
            )
            result = transaction_flow.make_transaction()
            assert result['status_code'] == 200
            assert result['data'] == 'ok'

    @patch('common.online_transactions.ExpensivePaymentGateway.make_transaction')
    def test_expensive_payment_gateway_using_function_calling(self, make_transaction, app_):
        """
        Test expensive payment gateway called with their own class make_transaction function
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                450,  # expensive amount
                security_code=321
            )
            transaction_flow.make_transaction()
            make_transaction.assert_called_once()

    @patch('common.online_transactions.make_request', side_effect=[
        {'data': 'ok', 'status_code': 500}, {'data': 'ok', 'status_code': 200}, {'data': 'ok', 'status_code': 200}
    ])
    @patch('common.online_transactions.CheapPaymentGateway.make_transaction', side_effect=[
        {'data': 'ok', 'status_code': 200}
    ])
    def test_expensive_payment_failure(self, make_transaction, make_request, app_):
        """
        Test expensive payment gateway failure with cheap payment gateway
        first side effect will throw failure that expensive_payment is unavailable and move to cheap payment gateway
        """
        with app_.test_request_context():  # this is for current_app.debug used at make_request for debugging purpose
            transaction_flow = OnlineTransaction(
                '5555555555554444',
                'syed hassan raza',
                datetime.datetime(2021, 12, 12),
                450,  # expensive amount
                security_code=321
            )
            result = transaction_flow.make_transaction()
            make_transaction.assert_called_once()
            assert result['status_code'] == 200
            assert result['data'] == 'ok'
