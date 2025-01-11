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

# fax 
# params -> company dict with  {name,address,phone and fax number }
# then a dict with fax information such as
# {ricipient fax number, status,confirmation id, date/time sent and delivered}
def generate_fax_confirmation(pdf_canvas, data):
    print("api.utils.generate_fax_confirmation.generate_fax_confirmation()")
    # Add content to the PDF
    # Header
    # Company Name
    pdf_canvas.setFont("Helvetica-Bold", 20)
    pdf_canvas.drawString(200, 750, data["company_name"])
    # Company Address
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(250, 730, data["company_address"])

    # Company Contanct
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(100, 700, f"Phone Number: {data["company_phone_number"]}")
    pdf_canvas.drawString(300, 700, f"Fax number: {data['company_fax_number']}")

    # Confirmation information

    pdf_canvas.setFont("Helvetica", 14)
    # Confirmation ID row
    pdf_canvas.drawString(100, 570, "Confirmation ID: ")
    pdf_canvas.drawString(250, 570, data["confirmation_id"])

    # Sender information row
    pdf_canvas.drawString(100, 540, "From: ")
    pdf_canvas.drawString(250, 540, data["sender"])

    # Recipient information row
    pdf_canvas.drawString(100, 510, "To: ")
    pdf_canvas.drawString(250, 510, data["recipient"])

    # Pages sent information row
    pdf_canvas.drawString(100, 480, "Pages Sent:")
    pdf_canvas.drawString(250, 480, data["total_pages"])

    # Pages delivered information row
    pdf_canvas.drawString(100, 450, "Pages Delivered: 3")
    pdf_canvas.drawString(250, 450, data["pages_delivered"])

    # Status Information row
    pdf_canvas.drawString(100, 420, "Status: ")
    pdf_canvas.drawString(250, 420, data["fax_status"])

    # Date/time fax sent row
    pdf_canvas.drawString(100, 390, "Time Sent")
    pdf_canvas.drawString(250, 390, data["fax_sent_time"])

    # Date/Time Fax received by recipient
    pdf_canvas.drawString(100, 360, "Time Delivered")
    pdf_canvas.drawString(250, 360, data["fax_delivered_time"])

    # Add a footer
    pdf_canvas.setFont("Helvetica-Oblique", 10)
    pdf_canvas.drawString(100, 50, "This is a system-generated document.")

    # Finalize the PDF and close the canvas
    pdf_canvas.showPage()
    pdf_canvas.save()

    return pdf_canvas