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


def attach_image(message, img_data):
    """A function that adds an image to the message."""
    from email.mime.image import MIMEImage

    image = MIMEImage(img_data, name="giphy.gif")
    image.add_header("Content-ID", "<image>")
    message.attach(image)


def verify_email(user_name, user_email, verification_link):
    """A function that sends email verification to new users."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender_email = "bookerapiteam@gmail.com"
    recipient_email = user_email
    recipient_name = user_name
    verification_link = verification_link
    subject = "Booker email verification."
    img_filename = "/app/templates/pictures/giphy.gif"

    img_data = open(img_filename, "rb").read()

    message_body = f"""<html>
    <body>
        <center><h3>Welcome to Booker🎉, {recipient_name}!</h3></center>
        <p>We are so pleased to have you with us.
        Click <a href="{verification_link}">here</a> to verify your account.</p>
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

    print("Email sent successfully!")
