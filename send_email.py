import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import sender_email, password, smtp_server, smtp_port


def send_email(file_path, name, receiver_email):
    mail = f""" <!doctype html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" 
    content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"> <meta 
    http-equiv="X-UA-Compatible" content="ie=edge"> <title>Document</title> </head> <body> <p>Hi, TNS Pay Team </p> 
    <p>Hi, {name}</p>
    <p>Welcome to our estate. Attached is your QR code. Keep it safe because it will be required for verification
    purpose</p> 
    <p>Kind regards,</p>
    <p>The SFTP script</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Smart Security Lock System"

    message.attach(MIMEText(mail, "html"))

    with open(file_path, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f"attachment; filename= {file_path}",
    )
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
