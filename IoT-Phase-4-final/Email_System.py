import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# The Light is ON at hh: mm time. (hh: mm means the current time)

def send_email_light():
    current_time = datetime.now().strftime("%H:%M")

    subject = "It's dark"
    body = f"The light is on at {current_time} time."
    sender = "arshsinghalt@gmail.com"
    recipients = ["arshmain24@gmail.com"]
    password = "kbzx epve kvim erhm"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

subject = "Turn fan on"
sender = "arshsinghalt@gmail.com"
recipient = "arshmain24@gmail.com"
password = "kbzx epve kvim erhm"
emailStatus = False
receiveStatus = False

def send_email_fan(temp_threshold, temperature):
    global sender, password, recipient, subject, emailStatus
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    body = f'The current temperature is {temperature}. Would you like to turn on the fan?'
    msg.attach(MIMEText(body, 'plain'))

    try:
        if emailStatus:
            return emailStatus
        elif temp_threshold < temperature and not emailStatus:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            text = msg.as_string()
            emailStatus = True
            server.sendmail(sender, recipient, text)
            server.quit()
            return "Email sent successfully!"
    except Exception as e:
        return "Error sending email:", str(e)


def receive_email_fan():
    global sender, password, recipient, receiveStatus

    if receiveStatus:
        return receiveStatus

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender, password)
        mail.select("inbox")

        # Search for unseen or unread emails only
        result, data = mail.search(None, "UNSEEN", "FROM", recipient)

        # If there are no unseen emails, return False
        if not data[0]:
            return False

        ids = data[0].split()
        # Fetch the latest unseen email
        latest_email_id = ids[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]

        email_message = email.message_from_bytes(raw_email)
        print("Subject:", email_message['Subject'])
        print("From:", email_message['From'])

        # Extract body
        body = extract_body_from_email(email_message)
        print("Body:")

        # Check if 'yes' is in the body
        if 'yes' in body.lower():
            print("yes")
            receiveStatus = True
        else:
            print("no")
            receiveStatus = False

        mail.close()
        mail.logout()
        return receiveStatus

    except Exception as e:
        print("Error receiving email:", e)
        return False


def extract_body_from_email(email_message):
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if "text/plain" in content_type:
                body += part.get_payload(decode=True).decode('utf-8', 'ignore')
    else:
        body = email_message.get_payload(decode=True).decode('utf-8', 'ignore')

    return body

def send_email_login(username):
    current_time = datetime.now().strftime("%H:%M")

    subject = "User logged in"
    body = f"User {username} entered at this time"
    sender = "arshsinghalt@gmail.com"
    recipients = ["arshmain24@gmail.com"]
    password = "kbzx epve kvim erhm"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

