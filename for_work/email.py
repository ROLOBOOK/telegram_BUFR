import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 


def send_email(body='Проверка успешна', subject='test'):
    fromaddr = "sender.bufr@gmail.com"
    mypass = "Fed1saerw7"
    toaddr = "fomenko@cao-ntcr.mipt.ru"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.sendmail(fromaddr, "fomenko.oleg@mail.ru", text)
    server.quit()

    print('Email is sender')
