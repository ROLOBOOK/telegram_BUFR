# !/usr/bin/env python3

from pybufrkit.renderer import FlatJsonRenderer
from pybufrkit.dataquery import NodePathParser, DataQuerent
from pybufrkit.decoder import Decoder
import os, MySQLdb, time, random, datetime
import conect_bd


today = datetime.datetime.now()
begintime = time.time()
minut = random.uniform(50,130)

print(f'Начало проверки: {today.strftime("%Y-%m-%d %H:%M")}')

def log_mistake(file_name, ex):
    ''' записывает в лог две переданые строки'''
    with open(f'{today.strftime("%Y-%m-%d")} log_mistake.txt', 'a') as mistake:
        mistake.write(f'{file_name} - {ex}\n')

def get_values_from_bufr(descriptor, key=0):
    ''' возвращает значение указаного дескриптора из разшифровоной телеграммы'''
    data = DataQuerent(NodePathParser()).query(bufr_message, descriptor).get_values(key)
    return data[0] if data else None

def decod_b(data):
    data = [chr(i) for i in data]
    return ''.join(data).replace(' ', '')

def get_data_for_info_pusk(bufr_message, kye=0):
    index_station = '{:03d}{:03d}'.fomrat(get_values_from_bufr("001001",kye),get_values_from_bufr("001002",kye))
    time_pusk = f'{get_values_from_bufr("004001",kye)}-{get_values_from_bufr("004002",kye)}-{get_values_from_bufr("004003",kye)} {get_values_from_bufr("004004",kye)}:{get_values_from_bufr("004005",kye)}:00'
    koordinat = f'{get_values_from_bufr("005001",kye)} {get_values_from_bufr("006001",kye)} {get_values_from_bufr("007030",kye)} {get_values_from_bufr("007031",kye)} {get_values_from_bufr("007007",kye)}'
    oborudovanie = f'{get_values_from_bufr("002011",kye)} {get_values_from_bufr("002013",kye)} {get_values_from_bufr("002014",kye)} {get_values_from_bufr("002003",kye)}'
    oblachnost = f'{get_values_from_bufr("008002",kye)} {get_values_from_bufr("002011",kye)} {get_values_from_bufr("002013",kye)} {get_values_from_bufr("002012",kye)}'
    sdvig_vetra = f'{get_values_from_bufr("031001",kye)}'
    metod_opredeleniy_visoti = f'{get_values_from_bufr("002191",kye)}'
    po_versia = decod_b(get_values_from_bufr("025061",kye)) if get_values_from_bufr("025061",kye) else None
    s_n_zonda = decod_b(get_values_from_bufr("001081",kye)) if get_values_from_bufr("001081",kye) else None
    algoritm_popravok_izmereniy_vlagnosti = f'{get_values_from_bufr("002017",kye)}'
    nesyshay_chastota = f'{get_values_from_bufr("002067",kye)}'
    datchik_davleniy = f'{get_values_from_bufr("002095",kye)}'
    datchik_temperatur = f'{get_values_from_bufr("002096",kye)}'
    datchik_vlagnosti = f'{get_values_from_bufr("002097",kye)}'
    nomer_nabludenia = f'{get_values_from_bufr("001082",kye)}'
    nomer_zondirovania = f'{get_values_from_bufr("001083",kye)}'
    fio_nabludateliy = decod_b(get_values_from_bufr("001095",kye)) if get_values_from_bufr("001095",kye) else None
    nazemnaiy_sistema_priema_signalov = f'{get_values_from_bufr("002066",kye)}'
    visota = f'{get_values_from_bufr("007007,kye")}'
    visota_anteni = f'{get_values_from_bufr("002102",kye)}'
    popravka_azimut = f'{get_values_from_bufr("025065",kye)}'
    popravka_ygl = f'{get_values_from_bufr("026066",kye)}'
    radio_ykritie = f'{get_values_from_bufr("002103",kye)}'
    configur_zonda = f'{get_values_from_bufr("002015",kye)}'
    configur_podveski_zonda = f'{get_values_from_bufr("002016",kye)}'
    proizvoditel_obolochki = f'{get_values_from_bufr("002080",kye)}'
    tip_obolochki = f'{get_values_from_bufr("002081",kye)}'
    massa_obolochki = f'{get_values_from_bufr("002082",kye)}'
    gaz_dly_napolnenia = f'{get_values_from_bufr("002084",kye)}'
    kolichestbo_gaza = f'{get_values_from_bufr("002085",kye)}'
    dlina_podvesa = f'{get_values_from_bufr("002086",kye)}'
    prichina_prikrashenia = f'{get_values_from_bufr("035035",kye)}'

    return [index_station, time_pusk, koordinat, oborudovanie, oblachnost, sdvig_vetra, metod_opredeleniy_visoti,
             po_versia, s_n_zonda, algoritm_popravok_izmereniy_vlagnosti, nesyshay_chastota, datchik_davleniy,
             datchik_temperatur, datchik_vlagnosti, nomer_nabludenia, nomer_zondirovania, fio_nabludateliy,
             nazemnaiy_sistema_priema_signalov, visota, visota_anteni, popravka_azimut, popravka_ygl, radio_ykritie, configur_zonda,
             configur_podveski_zonda, proizvoditel_obolochki, tip_obolochki, massa_obolochki, gaz_dly_napolnenia, kolichestbo_gaza, dlina_podvesa,
             prichina_prikrashenia]


# получаем файлы из папки "/folder_with_telegram/" 
try:
    files = [file for file in os.listdir(path="./folder_with_telegram/") if file[-3:] == 'bin']
except Exception as ex:
    log_mistake("ошибка получения списка телеграмм для: ", f'{ex}\n')
    print('Критическая ошибка, проверьте логи.')
    exit()

if not files:
    print('Не получены файлы для проверки')
    exit()

count_telegram = 0

for file_name in files:
    try:
        decoder = Decoder()
        with open(f'folder_with_telegram/{file_name}', 'rb') as ins: #
            bufr_message = decoder.process(ins.read())
    except Exception as ex:
        log_mistake(file_name, f'не декодирован, {ex}\n')

    json_data = FlatJsonRenderer().render(bufr_message)
    d = '{}-{:02d}-{:02d}'.format(json_data[1][-6], json_data[1][-5], json_data[1][-4])
    t = '{:02d}:{:02d}:{:02d}'.format(json_data[1][-3], json_data[1][-2], json_data[1][-1] )
    time_srok =  f'{d} {t}'


    for kye in range(len(json_data[3][2])):
        try:
            data_in_cao_info_pusk = get_data_for_info_pusk(bufr_message,kye)
            text_info = json_data[3][2][kye][-1].decode('utf-8') if type(json_data[3][2][kye][-1]) == bytes else None
            data_in_cao_info_pusk.append(time_srok)
            data_in_cao_info_pusk.append(text_info)
        except Exception as ex:
            log_mistake(file_name, ex)
            print(file_name, ex)
        if not data_in_cao_info_pusk:
            print(file_name, 'problems')
        try:
            conn = MySQLdb.connect(conect_bd.server, conect_bd.username,\
                               conect_bd.password, conect_bd.bd, charset="utf8")
            cursor = conn.cursor()

            cursor.execute('''
            INSERT IGNORE INTO cao2.info_pusk
            (index_station, time_pusk, koordinat, oborudovanie, oblachnost, sdvig_vetra, metod_opredeleniy_visoti, 
             po_versia, s_n_zonda, algoritm_popravok_izmereniy_vlagnosti, nesyshay_chastota, datchik_davleniy, 
             datchik_temperatur, datchik_vlagnosti, nomer_nabludenia, nomer_zondirovania, fio_nabludateliy, 
             nazemnaiy_sistema_priema_signalov, visota, visota_anteni, popravka_azimut, popravka_ygl, radio_ykritie, configur_zonda, 
             configur_podveski_zonda, proizvoditel_obolochki, tip_obolochki, massa_obolochki, gaz_dly_napolnenia, kolichestbo_gaza, dlina_podvesa, 
             prichina_prikrashenia, time_srok, text_info)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',data_in_cao_info_pusk)
            conn.commit()
        except Exception as ex:
            log_mistake(file_name, ex)
            print(file_name, ex)
        finally:
            conn.close()
        count_telegram+=1
        if  time.time() - begintime > minut:
            minut+=random.uniform(50,130)
            t = time.time() - begintime
            print('Сначала проверки прошло {:02d}:{:02d}:{:02d}, обработано {} телеграмм'.format(int(t//3600%24), int(t//60%60), int(t%60), count_telegram))

    try:
        os.rename(f'folder_with_telegram/{file_name}', f'folder_with_telegram/cheking_telegram/{file_name}')
    except Exception as ex:
        log_mistake(file_name, ex)



t = time.time() - begintime
print('Проверка закончена за {:02d}:{:02d}:{:02d}'.format(int(t//3600%24), int(t//60%60), int(t%60)))
try:
    with open(f'{today.strftime("%Y-%m-%d %H:%M")} log_mistake.txt', 'a') as mistake:
        print('проверьте файл с ошибками log_mistake.txt')
except:
    print('ошибок нет')
