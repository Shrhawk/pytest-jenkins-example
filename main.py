import os


def print_variable():
    user_email = os.getenv("USER_EMAIL")
    user_password = os.getenv("USER_PASSWORD")
    login_url = os.getenv("LOGIN_URL")
    success_url = os.getenv("SUCCESS_URL")
    print(user_email, user_password, login_url, success_url)

if __name__ == "__main__":
    print_variable()
