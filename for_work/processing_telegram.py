# !/usr/bin/env python3

from pybufrkit.dataquery import NodePathParser, DataQuerent
from pybufrkit.decoder import Decoder
import os, MySQLdb, time, random, datetime
import conect_bd


today = datetime.datetime.now()
def log_mistake(file_name, ex):
    ''' записывает в лог две переданые строки'''
    with open(f'{today.strftime("%Y-%m-%d %H:%M")} log_mistake.txt', 'a') as mistake:
        mistake.write(f'{file_name} - {ex}\n')

def get_values_from_bufr(descriptor):
    ''' возвращает значение указаного дескриптора из разшифровоной телеграммы'''
    return DataQuerent(NodePathParser()).query(bufr_message, descriptor).get_values(0)

def decod_b(data):
    data = [chr(i) for i in data]
    return ''.join(data)

list_for_base = ['index_station', 'time_pusk', 'koordinat', 'oborudovanie',\
                     'oblachnost', 'sdvig_vetra', 'metod_opredeleniy_visoti', 'po_versia',\
                     's_n_zonda', 'algoritm_popravok_izmereniy_vlagnosti',\
                     'nesyshay_chastota', 'datchik_davleniy', 'datchik_temperatur', \
                     'datchik_vlagnosti', 'text_info', 'nomer_nabludenia', \
                     'nomer_zondirovania', 'fio_nabludateliy', \
                     'nazemnaiy_sistema_priema_signalov', 'visota', 'visota_anteni', \
                     'popravka_azimut', 'popravka_ygl', 'radio_ykritie', 'configur_zonda', \
                     'configur_podveski_zonda', 'proizvoditel_obolochki', 'tip_obolochki',\
                     'massa_obolochki', 'gaz_dly_napolnenia', 'kolichestbo_gaza', \
                     'dlina_podvesa', 'prichina_prikrashenia'\
                     ]
    d

dict_descriptor = {
    'index_station': '001001 001002', \
    'time_pusk': '004001 004002 004003 004004 004005', \
    'koordinat': '005001 006001 007030 007031 007007 033024',\
    'oborudovanie': '002011 002013 002014 002003', \
    'oblachnost': '008002 020011 020013 020012',\
    'sdvig_vetra': '031001', 'metod_opredeleniy_visoti': '002191',\
    'po_versia': '025061', 's_n_zonda': '001081',\
    'algoritm_popravok_izmereniy_vlagnosti': '002017',\
    'nesyshay_chastota': '002067', 'datchik_davleniy': '002095',\
    'datchik_temperatur': '002096\t\t\t\t\t', 'datchik_vlagnosti': '002097',\
    'text_info': '12',\
    'nomer_nabludenia': '001082', 'nomer_zondirovania': '001083',\
    'fio_nabludateliy': '001095', 'nazemnaiy_sistema_priema_signalov': '002066',\
    'visota': '007007', 'visota_anteni': '002102', 'popravka_azimut': '025065',\
    'popravka_ygl': '026066', 'radio_ykritie': '002103', 'configur_zonda': '002015',\
    'configur_podveski_zonda': '002016', 'proizvoditel_obolochki': '002080',\
    'tip_obolochki': '002081', 'massa_obolochki': '002082',\
    'gaz_dly_napolnenia': '002084', 'kolichestbo_gaza': '002085',\
    'dlina_podvesa': '002086', 'prichina_prikrashenia': '035035'
  # 't': '004086',\
  # 'P': '007004', 'T': '012101', 'Td': '012103', 'H': '010-009',\
  # 'D': '011-001', 'V': '011-002', 'dLat': '005015', 'dLon': '006015',\
  # 'Flags': '008042',
}

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

for file_name in files:
    try:
        decoder = Decoder()
        with open(f'folder_with_telegram/{file_name}', 'rb') as ins: #
            bufr_message = decoder.process(ins.read())
    except Exception as ex:
        log_mistake(file_name, f'не декодирован, {ex}\n')

    json_data = FlatJsonRenderer().render(bufr_message)

    d = [get_values_from_bufr(dict_descriptor(text)) for text in list_for_base]





    try:
        conn = MySQLdb.connect(conect_bd.server, conect_bd.username,\
                               conect_bd.password, conect_bd.bd, charset="utf8")
        cursor = conn.cyrsor()

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
    finally:
        conn.close()
