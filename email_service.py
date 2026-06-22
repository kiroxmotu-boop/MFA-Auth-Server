import smtplib
from email.message import EmailMessage


SMTP_EMAIL = "YOUR_GMAIL@gmail.com"
SMTP_PASS = "YOUR_APP_PASSWORD"


def send_otp(receiver, otp):

    msg = EmailMessage()

    msg["Subject"] = "Your OTP Code"
    msg["From"] = SMTP_EMAIL
    msg["To"] = receiver

    msg.set_content(
        f"""
Your OTP is:

{otp}

This OTP expires in 5 minutes.
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            SMTP_EMAIL,
            SMTP_PASS
        )

        server.send_message(msg)

    print("OTP sent to", receiver)