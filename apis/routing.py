from flask import current_app

from apis.api_v1.routing_v1 import setup_v1_routes


def setup_api_routing():
    """
    Setup routes for the app
    :return:
    """
    current_app.url_map.strict_slashes = False  # allow trailing slash to urls/routes
    setup_v1_routes()
# new_branch_for_backport_test (commit1)
