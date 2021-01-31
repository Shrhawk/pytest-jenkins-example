from flask import Blueprint, current_app
from flask_restful import Api

from apis.api_v1.payment_process_api.api import ProcessPaymentApi


def setup_v1_routes():
    """
    Setup V1 routes
    :return:
    """
    api_v1_blue_print = Blueprint('api_v1', __name__)
    api = Api(api_v1_blue_print)
    api.add_resource(ProcessPaymentApi, '/process-payment')
    current_app.register_blueprint(api_v1_blue_print, url_prefix='/api/v1')
