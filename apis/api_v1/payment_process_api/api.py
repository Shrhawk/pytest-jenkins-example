from flask import current_app
from flask_restful import Resource

from apis.api_v1.payment_process_api.validation import request_parser
from common.constants import DEFAULT_RESPONSE
from common.online_transactions import OnlineTransaction


class ProcessPaymentApi(Resource):
    status_code = 200
    response_data = DEFAULT_RESPONSE

    def send_response(self):
        return self.response_data, self.status_code

    @current_app.auth.login_required
    def post(self):
        request_arguments = request_parser.parse_args()
        transaction_flow = OnlineTransaction(
            request_arguments.CreditCardNumber,
            request_arguments.CardHolder,
            request_arguments.ExpirationDate,
            request_arguments.Amount,
            security_code=request_arguments.SecurityCode
        )
        result = transaction_flow.make_transaction()
        self.status_code = result['status_code']
        self.response_data = result['data']
        return self.send_response()
# new_branch_for_backport_test (commit2)
