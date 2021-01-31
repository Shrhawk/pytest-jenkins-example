import optparse

from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.auth = HTTPBasicAuth()

with app.app_context():
    from apis.routing import setup_api_routing
    setup_api_routing()

if __name__ == '__main__':
    # Set up the command-line options
    default_host, default_port, debug_mode = '0.0.0.0', 5051, True
    parser = optparse.OptionParser()
    parser.add_option(
        "-H",
        "--host",
        help="Host of the Flask-app default: {host}".format(host=default_host),
        default=default_host
    )
    parser.add_option(
        "-P",
        "--port",
        help="Port for the Flask-app default: {port}".format(port=default_port),
        default=default_port
    )
    parser.add_option(
        "--nd",
        "--nodebug",
        action="store_false",
        dest="debug",
        help="Disable debug-mode for Flask-app",
        default=debug_mode
    )
    options, _ = parser.parse_args()
    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
