import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Turn fan on"
sender = "arshsinghalt@gmail.com"
recipient = "arshmain24@gmail.com"
password = "kbzx epve kvim erhm"
emailStatus = False
receiveStatus = False
json_file_path = "/home/arsh/Documents/IoT-Projects/IoT-Phase-2-final/current_date.json"

def send_email(temperature):
    global sender, password, recipient, subject, emailStatus, json_file_path
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    body = f'The current temperature is {temperature}. Would you like to turn on the fan?'
    msg.attach(MIMEText(body, 'plain'))

    try:
        if emailStatus:
            return emailStatus
        elif temperature > 22 and not emailStatus:
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

def receive_email():
    global sender, password, recipient, receiveStatus, json_file_path
    # print(receiveStatus)
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

        ids = data[0]
        id_list = ids.split()

        # Fetch the first unseen email
        first_email_id = id_list[0]

        result, data = mail.fetch(first_email_id, "(RFC822)")
        raw_email = data[0][1]

        email_message = email.message_from_bytes(raw_email)
        print("Subject:", email_message['Subject'])
        print("From:", email_message['From'])
        print("Body:")
        for part in email_message.walk():
            content_type = part.get_content_type()
            str(part.get("Content-Disposition"))
            print(str(part.get("Content-Disposition")))
            if "text/plain" in content_type:
                body = part.get_payload(decode=True)
                print(body)
                lowercase_body = body.decode('utf-8').lower()
                print(lowercase_body)
                if 'yes' in lowercase_body:
                    receiveStatus = True
                    # mail.store(first_email_id, '+FLAGS', '\\Seen')
                    mail.store(first_email_id, '+FLAGS', '\\Deleted')
                else:
                    receiveStatus = False
        mail.close()
        mail.logout()
        return receiveStatus
    except Exception as e:
        print("Error receiving email:", e)
        return False
