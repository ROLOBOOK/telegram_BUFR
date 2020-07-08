import smtplib, random,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(body='', subject='test', file=0):
    fromaddr = "sender.bufr@gmail.com"
    mypass = "Fed1saerw7"
    toaddr = "fomenko@cao-ntcr.mipt.ru"
#    toaddr = 'fomenko.oleg@mail.ru'
    body_list = ["~(>_<~)", "[+_+]","@(-_-)@", "(x_x)", "(^_~)", "(-_')"]
    if not body:
        body = body_list[random.randint(0,len(body_list)-1)]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['CC'] = 'fomenko.oleg@mail.ru'
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    filepath = '/home/bufr/bufr_work/telegram_BUFR/temp_check_files_get_index.txt' 
    if file and os.path.isfile(filepath):
        with open(filepath) as fp: # Открываем файл для чтени
            file = MIMEText(fp.read()) # Используем тип MIMEText
            fp.close()
            file.add_header('Content-Disposition', 'attachment', filename='temp_check_files_get_index.txt')
            msg.attach(file)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)

    server.send_message(msg)
    server.quit()

    print('Email is sender')
