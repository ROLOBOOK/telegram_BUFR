from pybufrkit.renderer import FlatTextRenderer, NestedTextRenderer
from pybufrkit.dataquery import NodePathParser, DataQuerent
from pybufrkit.decoder import Decoder
import sys,os,time,re, logging, datetime, MySQLdb
from progress.bar import IncrementalBar
from datetime import date, timedelta, datetime
from collections import Counter
from for_work.email import send_email

def del_duble(set_):
    double = [i for i in Counter([i[:2] for i in set_]).items() if i[1] > 1]
    list_double = [i[0][0] for i in double]
    list_for_del = set()
    for data in set_:
        if  data[0] in list_double and data[-2] == '__':
            list_for_del.add(data)
    for i in list_for_del:
        set_.remove(i)
    return set_


def get_list_file(days=2):
    # получаем вчерашню дату
    yesterday = date.today() - timedelta(days=days)
    year, month, day = yesterday.strftime('%Y.%m.%d').split('.')
    files = []
    os.chdir('/home/bufr/aero_bufr/res2')
    if year in os.listdir():
        os.chdir(year)
        if month in os.listdir():
            os.chdir(month)
            if day in os.listdir():
                os.chdir(day)
                if '0000' in os.listdir():
                    files.extend([f'./0000/{file}' for file in os.listdir('0000') if file.endswith('bin')])
                if '1200' in os.listdir():
                    files.extend([f'./1200/{file}' for file in os.listdir('1200') if file.endswith('bin')])

    return files

def get_last_h(list_):
    if list_:
        temp =  [int(i[6]) for i in  list_ if i and len(i) > 7 and i[6].isdigit()]
        if temp:
            return sorted(temp)[-1]
    return '-'

def get_metadate(file_name, data, time_srok):
    try:
        for_index = [parsing(i,data) for i in ('001001','001002')]
        index_station = '{:0>2}{:0>3}'.format(*for_index)

        for_time_pusk = [int(parsing(i, data)) for i in ('004001', '004002', '004003', '004004','004005', '004006')]
        time_pusk = '{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}'.format(*for_time_pusk)

        for_koordinate = [parsing(i, data) for i in ('005001', '006001', '007030', '007031', '007007')]
        koordinat = '{} {} {} {}'.format(*for_koordinate[:4])

        for_oborudovanie = [parsing(i,data) for i in ('002011', '002013', '002014', '002003')]
        oborudovanie = '{:0>3} {:0>2} {:0>3} {:0>2}'.format(*for_oborudovanie)

        for_oblachnost = [parsing(i,data) for i in ('008002', '020011', '020013', '020012')]
        oblachnost = '{} {} {} {}'.format(*for_oblachnost)

        list_descriptions = ['002191','025061', '001081', '002017', '002067', '002095',
                             '002096', '002097', '001082', '001083', '001095', '002066', '007007', '002102', '025065',
                             '026066', '002103', '002015', '002016', '002080', '002081', '002082', '002084', '002085', '002086',
                             '035035']
        and_lost = [parsing(i, data) for i in list_descriptions]
        text_info = parsing('205060', data)
        if text_info == '__':
            text_info = parsing('205011', data)

        return (index_station, time_srok, time_pusk, koordinat, oborudovanie, oblachnost) + tuple(and_lost) + (text_info,)
    except ValueError as ex:
        logging(file_name, ex)
        return 0

def get_telemetria(index_station, date_srok, telegram):
    #отсечь сдвиг ветра в коне телеграммы
    pattern = '031001 DELAYED DESCRIPTOR REPLICATION FACTOR'
    for_split_telemetry = re.split(pattern, telegram)
    # разделить на слои
    pattern = r'# --- \d{1,100} of \d{1,1000} replications ---'
    telemetry_list =  re.split(pattern, for_split_telemetry[0])

    list_descriptions = ['004086', '007004', '012101', '012103', '010009', '011001', '011002', '005015', '006015', '008042']
    # список по слоям
    return [(index_station, date_srok, *[parsing(descriptor, telemetry) for descriptor in list_descriptions]) for telemetry in telemetry_list[1:]]


def set_in_bd(meta_in_bd, tele_in_bd,last_H_in_bd):

    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
        cursor = conn.cursor()
        cursor.executemany('''INSERT IGNORE INTO cao_bufr_v2.releaseZonde
            (Stations_numberStation, time_srok, time_pusk, koordinat, oborudovanie, oblachnost, GEOPOTENTIAL_HEIGHT_CALCULATION_002191,
            SOFTWARE_IDENTIFICATION_AND_VERSION_NUMBER_025061, RADIOSONDE_SERIAL_NUMBER_001081,
            CORRECTION_ALGORITHMS_FOR_HUMIDITY_MEASUREMENTS_002017, RADIOSONDE_OPERATING_FREQUENCY_002067,
            TYPE_OF_PRESSURE_SENSOR_002095, TYPE_OF_TEMPERATURE_SENSOR_002096, TYPE_OF_HUMIDITY_SENSOR_002097,
            RADIOSONDE_ASCENSION_NUMBER_001082, descriptor_001083, descriptor_001095, descriptor_002066, descriptor_007007,
            descriptor_002102, descriptor_025065, descriptor_026066, descriptor_002103, descriptor_002015, descriptor_002016,
            descriptor_002080, descriptor_002081, descriptor_002082, descriptor_002084, descriptor_002085, descriptor_002086,
            descriptor_035035, text_info_ValueData_205060)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', meta_in_bd)
        conn.commit()
        bar = IncrementalBar('in_bd_bufr', max = len(tele_in_bd))
        for lines in tele_in_bd:
            bar.next()
            cursor.executemany('''INSERT IGNORE INTO cao_bufr_v2.content_telegram (Stations_numberStation, date, time, P, T, Td, H, D, V, dLat, dLon, Flags)
                                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',lines)
            conn.commit()
        bar.finish()
        cursor.executemany('''INSERT IGNORE INTO cao_bufr_v2.last_H (Stations_numberStation, time_srok, H) VALUES (%s,%s,%s)''', last_H_in_bd)
        conn.commit()
    except:
        logging('ошибка при загрузке в базу', 1)

    finally:
        conn.close()

def logging(file, ex):
#    ''' записывает в лог две переданые строки'''
#    today = datetime.datetime.now()
#    with open(f'{today.strftime("%Y-%m-%d")} log_mistake.txt', 'a') as mistake:
#        mistake.write(f'{file} - {ex}\n')
    pass


def parsing(pattern, data):
    result = re.search(r'{} .*'.format(pattern), data)
    if result:
        res = result.group().split()[-1]
        if res == "None":
            answer = '__'
        elif pattern in ('205060', '025061', '001081'):
            answer = result.group().split("b'")[-1][:-1].strip()
        elif pattern == '002067':
            answer = '{:0<7}'.format(round(float(result.group().split()[-1])/1000000,1))
        elif pattern == '007004':
            answer = '{:.2f}'.format(float(res)/100)
        elif pattern in  ('012101', '012103'):
            answer = '{:.1f}'.format(float(res) - 273.15)
        elif pattern in ('005015', '006015'):
            answer = '{:.4f}'.format(float(res))
        elif pattern == '205011':
            temp = '{} {}'.format(*result.group().split()[-2:])
            answer = re.search(r'\d+ \d+', temp)
            if answer:
                answer = answer.group()
        else:
            answer = result.group().split()[-1]
        return answer
    return '__'

def get_index_srok_from_bd():
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")
        cursor = conn.cursor()
        cursor.execute("SELECT Stations_numberStation,time_srok,time_pusk FROM cao_bufr_v2.releaseZonde")

        info_srok_in_bd = cursor.fetchall()
    except Exception as ex:
        log_mistake('индексы станций не получены', ex)
    finally:
        conn.close()
    result = set()
    for i in info_srok_in_bd:
        if not i[1] or not i[2]: continue
        t1 = i[1].strftime('%Y-%m-%d %H:%M:%S')
        t2 = i[2].strftime('%Y-%m-%d %H:%M:%S')
        result.add(f'{i[0]}:{t1}:{t2}')
    return result


def main(days=1, doubl=0, solo_file=0):
    dubl_bufr = {}
    files = get_list_file(days=days)

    if solo_file:
        files = [solo_file]
    if not files:
        print('Не получены файлы для проверки')
        exit()
    meta_in_bd = set()
    tele_in_bd = set()
    last_H_in_bd = set()
    info_srok_in_bd = get_index_srok_from_bd()
    bar = IncrementalBar('decode_bufr', max = len(files)) 

    for file_name in files:
        bar.next()

        try:
            decoder = Decoder()
            with open(file_name, 'rb') as ins: #
                bufr_message = decoder.process(ins.read())
            # декодируем телеграмму в текстовый файл
            text_bufr = NestedTextRenderer().render(bufr_message)
        except:
            ex = 'misk'
            logging(file_name, ex)
            continue



        # делим телеграмму на разделы
        pattern = r'<<<<<< section [0-9] >>>>>>'
        list_decod_bufr = re.split(pattern, text_bufr)
        words = ['year','month','day','hour','minute','second']
        date_list = [int(re.search(r'{} = \d{}'.format(word, '{0,5}'),
            list_decod_bufr[2]).group().split(' = ')[-1]) for word in words]
        date_srok = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(date_list[0],
                date_list[1], date_list[2], date_list[3], date_list[4], date_list[5])

        # если в бафре несколько телеграмм
        pettern_split_some_telegram = r'###### subset \d{1,1000} of \d{1,1000} ######'
        list_telegrams_in_bufr = re.split(pettern_split_some_telegram, list_decod_bufr[4])

        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
        cursor = conn.cursor()
        # получаем данные из телеграмм
        for telegram in list_telegrams_in_bufr:
            meta_info = get_metadate(file_name, telegram, date_srok)
            if not meta_info:
                continue


            # делим телеграмму на разделы
            pattern = r'<<<<<< section [0-9] >>>>>>'
            list_decod_bufr = re.split(pattern, text_bufr)
            words = ['year','month','day','hour','minute','second']
            date_list = [int(re.search(r'{} = \d{}'.format(word, '{0,5}'),
                list_decod_bufr[2]).group().split(' = ')[-1]) for word in words]
            date_srok = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(date_list[0],
                    date_list[1], date_list[2], date_list[3], date_list[4], date_list[5])

            # если в бафре несколько телеграмм
            pettern_split_some_telegram = r'###### subset \d{1,1000} of \d{1,1000} ######'
            list_telegrams_in_bufr = re.split(pettern_split_some_telegram, list_decod_bufr[4])

            # получаем данные из телеграмм
            for telegram in list_telegrams_in_bufr:
                meta_info = get_metadate(file_name, telegram, date_srok)
                if not meta_info:
                    continue
                meta_inf = f'{meta_info[0]}:{meta_info[1]}:[meta_info[2]'
                if meta_inf not in info_srok_in_bd:
                     meta_in_bd.add(meta_info)

                index_station = meta_info[0]

                if meta_inf not in dubl_bufr: dubl_bufr[meta_inf]=set()
                dubl_bufr[meta_inf].add(file_name)

                telemetry_info = get_telemetria(index_station, date_srok, telegram)
                if  telemetry_info:
                    last_H = (telemetry_info[-1][0],telemetry_info[-1][1], get_last_h(telemetry_info))
                    if last_H not in last_H_in_bd:
                        tele_in_bd.add(tuple(telemetry_info))
                        last_H_in_bd.add(last_H)




    bar.finish()
#удаляем дубли образованые первой и второй частью телеграмм
    meta_in_bd = del_duble(meta_in_bd)
    if doubl:
        return dubl_bufr

    if solo_file: #для теста отдельных файлов
        return meta_in_bd

    set_in_bd(meta_in_bd, tele_in_bd,last_H_in_bd)
    return len(meta_in_bd)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        begin = time.time()
        print(f'Проверка за вчерашнй день')
        count_bufr =  main(days=1)
        t = time.time()-begin
        print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
        yesterday = date.today() - timedelta(days=1)
        send_email(subject=f'В базу занесено  {count_bufr}, {yesterday.strftime("%d:%m:%Y")}.')
    elif len(sys.argv) == 2 and sys.argv[1] == 'help':
        print('''Возможные аргументы:\n
        YYYYMMDD - будет проведен анализ телеграмм за указаный день\n
        YYYYMMDD gui  - будет проведен анализ телеграмм за указаный день без подтверждения\n
        YYYYMMDD doubl - будет проведен анализ телеграмм и сформирован файл с количеством дублей в телеграммах\n
        YYYYMMDD YYYYMMDD  - будет проведен анализ телеграмм за указаный период\n
        YYYYMMDD YYYYMMDD gui  - будет проведен анализ телеграмм за указаный период без подтверждения\n
        help - будет распечатана справка по ключам\n
        ''')
    
    elif len(sys.argv) == 2 and sys.argv[1].isdigit() and len(sys.argv[1])==8:
        day_ago = sys.argv[1]
        y,m,d = int(day_ago[:4]),int(day_ago[4:6]), int(day_ago[6:8])
        try:
            day_chek = datetime(y,m,d)
        except:
            print('Вы ввели не правильные аргументы, используйте команду help')
            exit()
        sterday = datetime.now() - day_chek
        datenow = day_chek.strftime('%Y.%m.%d')
        answer = input(f'Начать проверку за {datenow}(y/n):')
        if answer in ('y','yes','да','д','ok'):
            print('start')
            begin = time.time()
            main(days=sterday.days)
            t = time.time()-begin
            print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
        else:
            print('введенно не првапильное число или вы отказались от проверки')

    elif len(sys.argv) == 3 and sys.argv[1].isdigit() and len(sys.argv[1])==8:
        d1 = sys.argv[1]
        try:
            date1 = datetime(int(d1[:4]), int(d1[4:6]), int(d1[6:8]))
        except:
           print('Вы ввели не правильные аргументы, используйте команду help')
           exit()
        if sys.argv[-1] == 'gui':
            sterday = datetime.now() - date1
            main(days=sterday.days)
        elif sys.argv[-1] == 'doubl':
            sterday = datetime.now() - date1
            datenow = date1.strftime('%Y.%m.%d')
            answer = input(f'Начать проверку дублей за {datenow}(y/n):')
            if answer not in ('y','yes','да','д','ok'):
                print('введенно не првапильное число или вы отказались от проверки')
                exit()
            print('start')
            begin = time.time()
            dubl_bufr = main(days=sterday.days, doubl=1)
            r = 'Проверка дублей\n'
            for  kye,valum in dubl_bufr.items():
                if len(valum) > 1:
                    s = ','.join([i.split('/')[-1] for i in valum])
                else:
                    continue
                r += f'станция, срок {kye}; количество повторов -  {len(valum)}, в файлаx: {s}\n\n'
            t = time.time()-begin
            os.chdir('/home/bufr/bufr_work/telegram_BUFR')
            with open(f'DOUBL',"a") as f:
                f.write(r)
                print(f'файл DOUBL - создан')
            print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
            exit()
        elif sys.argv[-1].isdigit() and len(sys.argv[-1])==8:
            d2 = sys.argv[2]
            try:
                date2 = datetime(int(d2[:4]), int(d2[4:6]), int(d2[6:8]))
            except:
                print('Вы ввели не правильные аргументы, используйте команду help')
                exit()

            num1 = datetime.now() - date1
            num2 = datetime.now() - date2
            dat1 = date1.strftime('%Y.%m.%d')
            dat2 = date2.strftime('%Y.%m.%d')
            answer = input(f'Начать проверку за {dat1}-{dat2}(y/n):')
            if answer in ('y','yes','да','д','ok'):
                for i in range(num2.days,num1.days+1):
                    main(days=i)
        else:
            print('Вы ввели не правильные аргументы, используйте команду help')


    elif len(sys.argv) == 4 and sys.argv[1].isdigit() and len(sys.argv[1])==8 and len(sys.argv[2])==8:
        d1 = sys.argv[1]
        d2 = sys.argv[2]
        try:
            date1 = datetime(int(d1[:4]), int(d1[4:6]), int(d1[6:8]))
        except:
            print('Вы ввели не правильные аргументы, используйте команду help')
            exit()
        if  not sys.argv[2].isdigit():
            print('Не верно введена дата окончания проверки')
            exit()
        try:
             date2 = datetime(int(d2[:4]), int(d2[4:6]), int(d2[6:8]))
        except:
            print('Вы ввели не правильные аргументы, используйте команду help')
            exit()
        num1 = datetime.now() - date1
        num2 = datetime.now() - date2
        dat1 = date1.strftime('%Y.%m.%d')
        dat2 = date2.strftime('%Y.%m.%d')
        if sys.argv[-1] == 'gui':
            for i in range(num2.days,num1.days+1):
                main(days=i)
        else:
            print('Вы ввели не правильные аргументы, используйте команду help')
            exit()
        answer = input(f'Начать проверку за {dat1}-{dat2}(y/n):')
        if answer in ('y','yes','да','д','ok'):
            for i in range(num2.days,num1.days+1):
                main(days=i)

    else:
        print('Вы ввели не правильные аргументы, используйте команду help')





exit()

if __name__ == '__main__':
    if (len(sys.argv) == 2 and sys.argv[1].isdigit()) or (len(sys.argv) == 3 and sys.argv[1].isdigit()):
        day_ago = sys.argv[1]
        y,m,d = int(day_ago[:4]),int(day_ago[4:6]), int(day_ago[6:8])
        day_chek = datetime(y,m,d)
        sterday = datetime.now() - day_chek
        datenow = day_chek.strftime('%Y.%m.%d')
        if sys.argv[-1] == 'gui':
            main(days=sterday.days)
        else:
            answer = input(f'Начать проверку за {datenow}(y/n):')
            if answer in ('y','yes','да','д','ok'):
                print('start')
                begin = time.time()
                main(days=sterday.days)
                t = time.time()-begin
                print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
            else:
                print('введенно не првапильное число или вы отказались от проверки')
    elif len(sys.argv) == 4 and sys.argv[1].isdigit():
        d1 = sys.argv[1]
        d2 = sys.argv[2]
        date1 = datetime(int(d1[:4]), int(d1[4:6]), int(d1[6:8]))
        if d2 == 'doubl':
            sterday = datetime.now() - date1
            datenow = date1.strftime('%Y.%m.%d')
            answer = input(f'Начать проверку дублей за {datenow}(y/n):')
            if answer not in ('y','yes','да','д','ok'):
                print('введенно не првапильное число или вы отказались от проверки')
                exit()
            print('start')
            begin = time.time()
            dubl_bufr = main(days=sterday.days, doubl=1)
            r = 'Проверка дублей\n'
            for  kye,valum in dubl_bufr.items():
                if len(valum) > 1:
                    s = ','.join([i.split('/')[-1] for i in valum])
                else:
                    continue
                r += f'станция, срок {kye}; количество повторов -  {len(valum)}, в файлаx: {s}\n\n'
            t = time.time()-begin
            os.chdir('/home/bufr/bufr_work/telegram_BUFR')
            with open(f'DOUBL',"a") as f:
                f.write(r)
                print(f'файл DOUBL - создан')
            print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
            exit()
        if  not sys.argv[2].isdigit():
            print('Не верно введена дата окончания проверки')
            exit()
        date2 = datetime(int(d2[:4]), int(d2[4:6]), int(d2[6:8]))
        num1 = datetime.now() - date1
        num2 = datetime.now() - date2
        dat1 = date1.strftime('%Y.%m.%d')
        dat2 = date2.strftime('%Y.%m.%d')
        if sys.argv[3] == 'gui':
            for i in range(num2.days,num1.days+1):
                main(days=i)
            exit()
        answer = input(f'Начать проверку за {dat1}-{dat2}(y/n):')
        if answer in ('y','yes','да','д','ok'):
            for i in range(num2.days,num1.days+1):
                main(days=i)

    else:
        begin = time.time()
        print(f'Проверка за вчерашнй день')
        count_bufr =  main(days=1)
        t = time.time()-begin
        print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
        yesterday = date.today() - timedelta(days=1)
        send_email(subject=f'В базу занесено  {count_bufr}, {yesterday.strftime("%d:%m:%Y")}.') 





