""" 1 Для начала сделай, пожалуйста, чтобы папка report_MMYYYY (MM - месяц,
YYYY - код) копировалась на ftp: cao-rhms.ru, monitor/radar в папку
maks/YYYY/MM-YYYY/report_MMYYYY
maks - эта папка постоянная
YYYY - эта папка создается в ручную, поэтому хорошо бы 1 января чтобы
она создавалась
MM-YYYY - эта папка создается в ручную, поэтому хорошо бы 1 числа чтобы
она создавалась
2. еще он хотел, чтобы архив bufr за последние сутки копировался в туже
папку maks/YYYY/MM-YYYY/bufr и через сутки он туда удалялся
"""


from ftplib import FTP
from datetime import datetime
import os


def main():
    server = 'cao-rhms.ru'
    login = 'monitor'
    pas = 'radar'

    def goto(ftp,path):
        """переходим по пути  path, если ошибка создаем папку и переходим в созданую папку"""
        try:
            ftp.cwd(path)
        except:
            ftp.mkd(path)
            ftp.cwd(path)

    ftp = FTP(server)
    ftp.login(login, pas)

    ftp.cwd('maks')

    today = datetime.now()
    year = f'{today.year:4}'
    month = f'{today.month:02}'

    goto(ftp, year)
    goto(ftp,f'{month}-{year}')
    goto(ftp, f'report_{month}{year}')
    # мы в папке maks/YYYY/MM-YYYY/report_MMYYY

    begin_pwd_local = os.getcwd()
    os.chdir(f'/home/bufr/reports/report_{month}{year}')
    # получим фалы из папки home/bufr/reports/report_MMYYYY и отправим их на сервер фтп
    files_list = os.listdir()
    folders = [folder for folder in files_list if os.path.isdir(folder)]
    for folder in folders:
        try:
            ftp.mkd(folder)
        except:
            pass
        files_list.extend([f'{folder}/{file}' for file in os.listdir(folder)])
    
    print(files_list)
      
    for file in files_list:
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                ftp.storbinary("STOR"+file, f, 1024)
    
    print('files was send')

    ftp.close()
    os.chdir(begin_pwd_local)

if __name__ == '__main__':
    main()

