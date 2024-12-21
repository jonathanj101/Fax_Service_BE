# Import modules
from django.core.mail import send_mail
import random


def generate_random_password(length=30):
    # GENERATE RANDOM PASSWORD, IN CASE USER FORGOT PASSWORD
    print("helpers/services/services/generate_random_password")
    text = ""
    random_number = random.random() * length
    random_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+"
    for char in range(length):
        text += random_chars[random.randint(
            0, len(random_chars)-1)]
    return text


def forgot_password_notify_user(subject, message, subject2, user_email, username):
    # NOTIFY USER WHEN FORGOT PASSWORD VIA EMAIL
    print("herlpers/services/services/forgot_password_notify_user()")

    html_message = f"""
    <h1>
        Forgot Password
    </h1>
    <br/>
    <p>
    Dear {username},
        We received a reset password request. Please click the link below to continue to reset password!
    </p>
    <h3>
    </h3>
    <br/>
    <button>
        <a href="link to reset password page on the client side">
            reset password
        </a>
    </button>
    """
    # print(html_message)
    mailed = send_mail(
        subject,
        message,
        subject2,
        [user_email],
        False,
        None,
        None,
        None,
        html_message
    )
    if mailed:
        return True
    return False


def reset_password_notify_user(subject, message, subject2, user_mail, username):
    # NOTIFY USER WHEN RESET PASSWORD VIA EMAIL
    print("helpers/services/services/reset_password_notify_user()")
    html_message = f"""
    <h1>
        Password Reset Successfully!
    </h1>
    <br/>
    <p>
    Dear {username},
        Your password have been reset successfully! Now, try to log in again with the new password you just set up!
    </p>
    <h3>
    </h3>
    <br/>
    """
    mailed = send_mail(
        subject,
        message,
        subject2,
        [user_mail],
        False,
        None,
        None,
        None,
        html_message
    )
    if mailed:
        return True,
    return False


def split_bearer_value(token):
    # print(token)
    if token:

        token_striped = token.strip("Bearer")
        token_striped = token_striped.strip(" ")
        # print(token_striped)
        return token_striped
    else:
        return ""
