import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime
import random
import string
import os


def verify_email(user_name, user_email, verification_link):
    """A function that sends email verification to new users."""

    path = os.getenv("PWD")
    sender_email = "bookerapiteam@gmail.com"
    recipient_email = user_email
    recipient_name = user_name
    subject = "Booker email verification."
    img_filename = f"{path}/resources/giphy.gif"

    img_data = open(img_filename, "rb").read()

    message_body = f"""<html>
    <body>
        <center><h3>Welcome to Booker🎉, {recipient_name}!</h3></center>
        <p>We are so pleased to have you with us.
        Click {verification_link} to verify your account.</p>
        <img src="cid:image" alt="Happy">
        <p>Please keep in touch and reach out to us for any help needed.</p>
        <p>Feel at home and checkout the available workspaces.</p>
    </body>
    </html>"""

    message = MIMEMultipart("related")
    message.attach(MIMEText(message_body, "html"))

    attach_image(message, img_data)

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("bookerapiteam@gmail.com", "wuzg nnvd eztu ygck")
        server.sendmail(sender_email, recipient_email, message.as_string())


def attach_image(message, img_data):
    """A function that adds an image to the message."""
    from email.mime.image import MIMEImage

    image = MIMEImage(img_data, name="giphy.gif")
    image.add_header("Content-ID", "<image>")
    message.attach(image)


def send_password(user_name, user_email, temporary_password):
    """A function that sends the temporary password in case of password reset."""

    sender_email = "bookerapiteam@gmail.com"
    recipient_email = user_email
    recipient_name = user_name
    subject = "Booker password reset verification."

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


def generate_password():
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(all_characters, k=6))
    return password


def set_dict(initial_list, result_dict):
    """A function that sets a dictionary from a given list of objects."""
    result_dict.update(
        dict(
            zip(
                map(
                    lambda item: f"{item.__class__.__name__}.{item.id}",
                    initial_list,
                ),
                initial_list,
            )
        )
    )


def hash_to_sha256(string):
    """A function that hashes a given string to sha1."""
    import hashlib

    hashed_string = hashlib.sha256(string.encode()).hexdigest().lower()
    return hashed_string


def validate_fields(fields, data):
    """A function that takes two dicts and compares them and returns the missing
    and the extra fields."""
    fields_keys = set(fields.keys())
    data_keys = set(data.keys())
    error_str = ""
    if fields_keys != data_keys:
        if fields_keys - data_keys:
            error_str += f"{', '.join(fields_keys- data_keys)} missing"
        if data_keys - fields_keys:
            error_str += " and " if error_str else ""
            error_str += f"{', '.join(data_keys- fields_keys)} do not exist"
    return error_str


def check_schedules(schedules_dict):
    """A function that checks the validity of the schedule dictionary."""
    from app.utils.schedules import schedules

    if set(schedules_dict.keys()) != {"days"}:
        return "Make sure you set up the key [days]."

    for day, time in schedules_dict["days"].items():
        if not day or day not in schedules["days"].keys():
            return "Make sure you set up the days correctly."
        if time.keys():
            for item in list(time.keys()):
                if item not in ["from", "to", "break"]:
                    return "The data keys in each day should be one of the following: [from], [to], [break]"
                try:
                    datetime.strptime(time[item], "%H:%M").time()
                    if item in ["from", "to"]:
                        schedules["days"][day][item] = time[item]
                    else:
                        schedules["days"][day]["break"] = {
                            "from": time["break"]["from"],
                            "to": time["break"]["to"],
                        }
                except (ValueError, TypeError):
                    return "Make sure you set up the times correctly : %H:%M."
    return schedules


def send_attachment(recipient_name, recipient_email, content, subject):
    """A function that sends attachments to users."""
    sender_email = "bookerapiteam@gmail.com"

    message_body = f"""<html>
    <body>
        <center><h3>Hello {recipient_name}!</h3></center>
        <p>{subject}</p>
        <p>Please keep in touch and reach out to us for any help needed.</p>
        <p>Feel at home and checkout the available workspaces.</p>
    </body>
    </html>"""

    message = MIMEMultipart()
    message.attach(MIMEText(message_body, "html"))

    attachment_part = MIMEApplication(content)
    attachment_part.add_header(
        "Content-Disposition", "attachment", filename="invoice.pdf"
    )
    message.attach(attachment_part)

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("bookerapiteam@gmail.com", "wuzg nnvd eztu ygck")
        server.sendmail(sender_email, recipient_email, message.as_string())
