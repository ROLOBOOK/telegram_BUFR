from pybufrkit.renderer import FlatTextRenderer, NestedTextRenderer
from pybufrkit.dataquery import NodePathParser, DataQuerent
from pybufrkit.decoder import Decoder
import os,time,re, logging, datetime, MySQLdb, paramiko
from progress.bar import IncrementalBar
from datetime import date, timedelta
from for_work.ssh_connect import server,name,password,port


def get_list_file():
    # получаем вчерашню дату
    yesterday = date.today() - timedelta(days=1)
    year, month, day = yesterday.strftime('%Y.%m.%d').split('.')

    # подключаемся к серверу с телеграммами
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #избежать проблем с клчючем шифрования
    #ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    ssh.connect(server,username=name,password=password, port=port)
    print(f'connect to server {server}')
    ftp=ssh.open_sftp()
    files = []
    if year in ftp.listdir():
        ftp.chdir(year)
        if month in ftp.listdir():
            ftp.chdir(month)
            if day in ftp/listdir():
                ftp.chdir(day):
                if '0000' in ftp/listdir():
                    files.extend([f'./0000/{file}' for file in ftp.listdir('0000') if file.endswith('bin')])
                if '1200' in ftp/listdir():
                    files.extend([f'./1200/{file}' for file in ftp.listdir() if file.endswith('bin')])
    
    return files


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


def set_in_bd(meta_in_bd, tele_in_bd):

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
		
		
		
        for lines in tele_in_bd:
            cursor.executemany('''INSERT IGNORE INTO cao_bufr_v2.content_telegram (Stations_numberStation, date, time, P, T, Td, H, D, V, dLat, dLon, Flags)
                                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',lines)
            conn.commit()

    except:
        logging('ошибка при загрузке в базу', 1)

    finally:
        conn.close()

def logging(file, ex):
    ''' записывает в лог две переданые строки'''
    with open(f'{today.strftime("%Y-%m-%d")} log_mistake.txt', 'a') as mistake:
        mistake.write(f'{file} - {ex}\n')

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
        else:
            answer = result.group().split()[-1]
        return answer
    return '__'

def get_index_srok_from_bd():
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")
        cursor = conn.cursor()
        cursor.execute("SELECT Stations_numberStation,time_srok FROM cao_bufr_v2.releaseZonde")

        info_srok_in_bd = cursor.fetchall()
    except Exception as ex:
        log_mistake('индексы станций не получены', ex)
    finally:
        conn.close()
    return info_srok_in_bd



def main():
    files = get_list_file()
    if not files:
        print('Не получены файлы для проверки')
        exit()
    meta_in_bd = set()
    tele_in_bd = set()

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
            if not meta_info or meta_info in info_srok_in_bd:
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
            if not meta_info or meta_info in info_srok_in_bd:
                continue

            meta_in_bd.add(meta_info)

            index_station = meta_info[0]
            telemetry_info = get_telemetria(index_station, date_srok, telegram)

            tele_in_bd.add(tuple(telemetry_info))


        # перемещаем проверенный файл
        # os.rename(f'folder_with_telegram/{file_name}', f'folder_with_telegram/checking_files/{file_name}')
    bar.finish()
    set_in_bd(meta_in_bd, tele_in_bd)

if __name__ == '__main__':

    today = datetime.datetime.now()
    begin = time.time()
    main()
    t = time.time()-begin
    print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))





