import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# The Light is ON at hh: mm time. (hh: mm means the current time)

def send_email():
    current_time = datetime.now().strftime("%H:%M")

    subject = "It's dark"
    body = f"The Light is ON at {current_time} time."
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


