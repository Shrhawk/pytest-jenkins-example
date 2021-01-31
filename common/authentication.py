from flask import current_app

USER_CREDENTIALS = {
    "admin": "admin"
}


@current_app.auth.verify_password
def verify(username, password):
    """
    Verify the basic auth credentials
    :param username:
    :param password:
    :return:
    """
    if not (username and password):
        return False
    return USER_CREDENTIALS.get(username) == password
