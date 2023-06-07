import os


def print_variable():
    user_email = os.getenv("USER_EMAIL")
    user_password = os.getenv("USER_PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    success_url = os.getenv("SUCCESS_URL")

if __name__ == "__main__":
    print_variable()
