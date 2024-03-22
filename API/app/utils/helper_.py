import random
import string


def generate_password():
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(all_characters, k=6))
    return password


def send_password(user_name, user_email, temporary_password):
    """A function that sends email verification to new users."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import os

    sender_email = "bookerapiteam@gmail.com"
    recipient_email = user_email
    recipient_name = user_name
    subject = "Booker email verification."

    message_body = f"""<html>
    <body>
        <center><h3>Hi {recipient_name}!</h3></center>
        <p>This is your temporary password <strong>{temporary_password}</strong> you can use it once, it will expire in 10 min</p>
        <p>Please keep in touch and reach out to us for any help needed.</p>
        <p>Feel at home and checkout the available workspaces.</p>
    </body>
    </html>"""

    message = MIMEMultipart("related")
    message.attach(MIMEText(message_body, "html"))


    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("bookerapiteam@gmail.com", "wuzg nnvd eztu ygck")
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully!")
